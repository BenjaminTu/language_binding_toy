from aws import *
from input_stream_py import InputStream
import struct

aws_crt_init()
print("initiated")
# crt testing
pt = aws_crt_mem_acquire(100)
aws_crt_mem_release(pt)

key = b'TESTSECRETaccesskeyThatDefinitelyDoesntWork'
token = b'ThisIsMyTestSessionTokenIMadeItUpMyself'
key_id = b'TESTAWSACCESSKEYID'

# credentials_options testing
new_cred = aws_crt_credentials_options_new()
aws_crt_credentials_options_set_access_key_id(new_cred, key_id, len(key_id))
aws_crt_credentials_options_set_secret_access_key(new_cred, key, len(key))
aws_crt_credentials_options_set_session_token(new_cred, token, len(token))
aws_crt_credentials_options_set_expiration_timepoint_seconds(new_cred, 42)
print("Credentials options successfully created")

# credentials testing
pt = aws_crt_credentials_new(new_cred)
aws_crt_credentials_release(pt)
aws_crt_credentials_options_release(new_cred)
print("Credentials successfully created")

# credentials_provider_static_options testing
new_cred_option = aws_crt_credentials_provider_static_options_new()
aws_crt_credentials_provider_static_options_set_access_key_id(new_cred_option, key_id, len(key_id))
aws_crt_credentials_provider_static_options_set_secret_access_key(new_cred_option, key, len(key))
aws_crt_credentials_provider_static_options_set_session_token(new_cred_option, token, len(token))
print("Credentials Provider Static Options successfully created")

# credentials_provider testing
pt = aws_crt_credentials_provider_static_new(new_cred_option)
aws_crt_credentials_provider_release(pt)
aws_crt_credentials_provider_static_options_release(new_cred_option)
print("Credentials Provider successfully created")

# event group testing
option = aws_crt_event_loop_group_options_new()
aws_crt_event_loop_group_options_set_max_threads(option, 10)
pt = aws_crt_event_loop_group_new(option)
aws_crt_event_loop_group_release(pt)
aws_crt_event_loop_group_options_release(option)
print("Event Group successfully created")


blob = struct.pack(">I", 4) + b'host' + struct.pack(">I", 16) + b's3.amazonaws.com'
# http testing
aws_crt_http_headers_new_from_blob(blob, len(blob))
aws_crt_http_message_new_from_blob(blob, len(blob))
aws_crt_clean_up()
print("cleaned up")