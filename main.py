import json
import logging
import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential, ClientSecretCredential

# 1. setup the vault and secret information
vault_url = "https://XXXXX.vault.azure.net/"
# Please replace secret name to your secret.
secret_list = ["secret_1","secret_2"]

# 2. Setup the Azure Crediential type for using the SDK.

# [ClientSecretCredential ]
#   General Application token base login method for using API.
#   1. Utilize AzureAD application to get access to AzureAPI without login via Azure CLI

# [DefaultAzureCredential]
# # Login via Azure CLI (Azure CLI keep the token)
#   1. Run the `az login` command first to get the token to access API
#    https://learn.microsoft.com/en-us/azure/key-vault/secrets/quick-create-python?tabs=azure-cli
# DefaultAzureCredential
#   credential = DefaultAzureCredential()

# 1. ClientSecretCredentail
tenant_id="XXXXXX"
client_id="XXXXXXX"
client_secret="XXXXXXX"
credential = ClientSecretCredential(tenant_id=tenant_id, client_id=client_id, client_secret=client_secret)

# 3. Generate client with crediential to use API
client = SecretClient(vault_url=vault_url, credential=credential)

# 4. Get secret from Azure Vault
secret = client.get_secret(secret_name)

# 5. Process secret value to the JSON format compatible with Datadog-agent.
for secret_name in secret_list:
    try:
        secret = client.get_secret(secret_name)
    except ResourceNotFoundError as e:
        secret_output[secret_name] = {"value": "", "error": str(e)}
    else:
        secret_output[secret_name] = {"value": secret.value}

print(json.dumps(secret_output, indent=None))
