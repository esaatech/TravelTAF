import secrets
import string

def generate_verify_token(length=32):
    """Generate a secure random token"""
    alphabet = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(alphabet) for _ in range(length))
    print(f"\nYour WhatsApp Webhook Verify Token: {token}\n")
    print("Add this to your .env file as:")
    print(f"WHATSAPP_VERIFY_TOKEN={token}\n")
    
if __name__ == "__main__":
    generate_verify_token() 