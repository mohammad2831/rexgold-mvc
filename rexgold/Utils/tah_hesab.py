# import requests
# import json
# import ssl
# from urllib3 import PoolManager
# from urllib3.util.ssl_ import create_urllib3_context
# from requests.adapters import HTTPAdapter
# from urllib3.poolmanager import PoolManager
# from decouple import config


# class SSLAdapter(HTTPAdapter):
#     def __init__(self, ssl_context=None, **kwargs):
#         self.ssl_context = ssl_context
#         super().__init__(**kwargs)

#     def init_poolmanager(self, *args, **kwargs):
#         # Pass the custom SSL context to the pool manager
#         kwargs['ssl_context'] = self.ssl_context
#         return super().init_poolmanager(*args, **kwargs)


# def create_ssl_context():
#     context = create_urllib3_context()
#     context.set_ciphers('DEFAULT')
#     context.options |= ssl.OP_NO_TLSv1_3

#     context.check_hostname = False
#     context.verify_mode = ssl.CERT_NONE

#     return context


# def send_data_to_tah_hesab(action, data):
# payload = json.dumps({
#     action: data
# })

#     headers = {
#         'Authorization': f"Bearer {config('TAHHESABTOKEN')}",
#         'DBName': "TahesabDB",
#         # 'Content-Type': "application/json",
#         # 'User-Agent': "PostmanRuntime/7.15.2",
#         # 'Accept': "*/*",
#         # 'Cache-Control': "no-cache",
#         # 'Host': "127.0.0.1:8081",
#         # 'Accept-Encoding': "gzip, deflate",
#         # 'Connection': "keep-alive",
#         # 'cache-control': "no-cache"
#     }

#     try:

#         session = requests.Session()
#         adapter = SSLAdapter(ssl_context=create_ssl_context())
#         session.mount('https://', adapter)

#         response = session.post(config('TAHHESABURL'), data=payload, headers=headers, verify=False)
#         response.raise_for_status()

#         return response.text

#     except requests.exceptions.RequestException as e:
#         print(f"An error occurred: {e}")
#         pass


import json
import uuid
import asyncio
import warnings  # It's good practice to keep imports if they might be used (e.g., for InsecureRequestWarning)

# Assuming these are from your Django Channels setup
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


# Suppress InsecureRequestWarning for local testing (remove in production)
# from urllib3.exceptions import InsecureRequestWarning # Import if you uncomment the filter
# warnings.filterwarnings('ignore', category=InsecureRequestWarning)

# Define custom exception if it's not defined elsewhere
class AgentTimeoutError(Exception):
    """Custom exception for agent timeouts."""
    pass


def call_agent(action: str, data=None, *, group="tah_agents", timeout: float = 60):
    """
    Synchronous helper that does an RPC-style round-trip over Channels.

    Parameters
    ----------
    action      – string understood by the worker (e.g. "getmandehesabbycode")
    data        – payload you want to pass (str / list / dict / None)
    group       – channel-layer group where workers are listening
    timeout     – seconds to wait for the reply

    Returns
    -------
    The actual data payload from the agent's "tah_hesab" field.

    Raises
    ------
    RuntimeError        if the channel layer is not configured.
    AgentTimeoutError   if no worker responded within *timeout* seconds.
    Exception           for other errors during processing or if the response format is unexpected.
    """
    print(f"call_agent invoked with action: '{action}', data: {data}, group: '{group}', timeout: {timeout}s")

    channel_layer = get_channel_layer()
    if channel_layer is None:
        # This is a critical setup error.
        print("Error: Channel layer is not configured.")
        raise RuntimeError("Channel layer not configured properly")

    # Generate a unique channel name for the reply and a correlation ID for the request.
    reply_chan_base = "reply_"  # Base name for reply channel
    reply_chan = async_to_sync(channel_layer.new_channel)(reply_chan_base)
    corr_id = uuid.uuid4().hex

    # Ensure data is JSON-serializable. If not, convert to string as a fallback.
    # This might not be ideal for all data types but handles basic cases.
    if data is not None:
        try:
            json.dumps(data)
        except TypeError as e:
            print(f"Warning: Data for action '{action}' is not JSON-serializable: {e}. Converting to string.")
            data = str(data)

    # Construct the job message to be sent to the agent group.
    # 'origin' is used by DataConsumer to route the reply back to this 'reply_chan'.
    job = {
        "type": "agent.work",  # Routed to DataConsumer.agent_work
        "reply_to": reply_chan,  # Channel for this specific call to receive its reply
        "correlation_id": corr_id,  # Unique ID for this request-response cycle
        "action": action,
        "data": data or "",  # Ensure data is not None; use empty string if it is.
        "origin": reply_chan,  # DataConsumer uses this to know where to send the agent's final response
    }

    try:
        print(f"Sending job (corr_id: {corr_id}) to group '{group}': {json.dumps(job, indent=2)}")
        async_to_sync(channel_layer.group_send)(group, job)
    except Exception as e:
        # Catch any exception during the send operation.
        print(f"Error sending job to group '{group}': {e}")
        raise  # Re-raise the exception to be handled by the caller.

    received_msg = None  # Initialize for clarity
    try:
        print(f"Waiting for response on dedicated channel: '{reply_chan}' (corr_id: {corr_id}) for up to {timeout}s...")
        # Wait for a message on the reply channel.
        received_msg = async_to_sync(asyncio.wait_for)(
            channel_layer.receive(reply_chan),
            timeout=timeout
        )
        print(f"Raw message received on '{reply_chan}' (corr_id: {corr_id}): {json.dumps(received_msg, indent=2)}")

        # Process the received message based on the expected structure from DataConsumer.
        if received_msg and received_msg.get("type") == "ui.reply":
            agent_response_bundle = received_msg.get("message")

            if agent_response_bundle:
                # Verify the original correlation ID to ensure it's the response for our request.
                if agent_response_bundle.get("original_correlation_id") != corr_id:
                    # This is a critical error, indicating a mix-up in responses.
                    error_detail = (f"Correlation ID mismatch. Expected '{corr_id}', "
                                    f"got '{agent_response_bundle.get('original_correlation_id')}'.")
                    print(f"Error: {error_detail}")
                    raise Exception(error_detail)  # Use a more specific error if available

                # Extract the actual payload from the "tah_hesab" field.
                tah_hesab_payload = agent_response_bundle.get("tah_hesab")

                if tah_hesab_payload is None:
                    # The 'tah_hesab' field is expected. If missing, it's an issue.
                    print("Error: 'tah_hesab' field is missing in the agent response bundle.")
                    raise Exception("'tah_hesab' field is missing in the agent response bundle.")

                print(
                    f"Successfully extracted 'tah_hesab' payload (corr_id: {corr_id}): {json.dumps(tah_hesab_payload, indent=2)}")

                # The 'tah_hesab_payload' is the final result from the agent.
                # It might contain its own error structure (e.g., {"status": "error", "detail": ...})
                # which should be handled by the caller of call_agent.
                return tah_hesab_payload
            else:
                # The "message" field within "ui.reply" was missing.
                print("Error: The 'message' field was missing in the agent's 'ui.reply' message.")
                raise Exception("The 'message' field was missing in the agent's 'ui.reply' message.")
        else:
            # The received message was not of the expected type or was empty.
            print(
                f"Error: Unexpected message type or empty message received. Expected type 'ui.reply'. Got: {received_msg}")
            raise Exception(
                f"Unexpected message type or empty message received. Expected 'ui.reply'. Got: {type(received_msg)}")

    except asyncio.TimeoutError as e:
        # Timeout occurred while waiting for the response.
        print(f"Timeout: No response received on '{reply_chan}' (corr_id: {corr_id}) within {timeout}s.")
        raise AgentTimeoutError(
            f"No agent answered or replied on '{reply_chan}' (corr_id: {corr_id}) within {timeout}s") from e
    except Exception as e:
        # Catch any other exceptions during message processing.
        print(f"Error processing response on '{reply_chan}' (corr_id: {corr_id}): {e}")
        # Log the received message if it was populated, for debugging.
        if received_msg:
            print(f"Content of received_msg when error occurred: {json.dumps(received_msg, indent=2)}")
        raise  # Re-raise the caught exception.








# class HomeView(TemplateView):
#     template_name = "home.html"
#
#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#
#         try:
#             ctx["agent_data"] = call_agent(
#                 action="DoListNameSekeh",
#                 data=[{"id": 101, "name": "Triggered from HomeView"}],
#                 timeout=5,
#             )
#         except AgentTimeoutError as exc:
#             ctx["agent_data"] = None
#             ctx["error"] = str(exc)
#
#         return ctx






