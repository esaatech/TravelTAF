from dotenv import load_dotenv
load_dotenv()

from email_service import EmailManager

def test_email_service():
    email_manager = EmailManager()
    
    # Test data
    test_data = {
        'full_name': 'Test User',
        'email': 'esaathings@gmail.com',
        'target_countries': ['Canada', 'Australia'],
        'preferred_program': 'Masters in Computer Science',
        'timeline': '6 months'
    }
    
    print("Testing study abroad email...")
    success, message = email_manager.send_study_abroad_confirmation(test_data)
    print(f"Study abroad email: {'✅' if success else '❌'} {message}")
    
    print("\nTesting moving abroad email...")
    success, message = email_manager.send_moving_abroad_confirmation(test_data)
    print(f"Moving abroad email: {'✅' if success else '❌'} {message}")

if __name__ == "__main__":
    test_email_service() 