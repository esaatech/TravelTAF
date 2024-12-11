import firebase_admin
from firebase_admin import credentials, firestore
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class FirestoreManager:
    def __init__(self):
        if not firebase_admin._apps:
            BASE_DIR = Path(__file__).resolve().parent.parent
            CRED_PATH = os.path.join(BASE_DIR, 'firebase-credentials.json')
            
            try:
                if os.path.exists(CRED_PATH):
                    cred = credentials.Certificate(CRED_PATH)
                else:
                    cred = credentials.ApplicationDefault()
                
                firebase_admin.initialize_app(cred)
                logger.info("Firebase initialized successfully")
                
            except Exception as e:
                logger.error(f"Firebase initialization error: {str(e)}")
                raise

        try:
            self.db = firestore.client()
            # Test the connection
            self.db.collection('test').document('test').get()
            logger.info("Firestore connection successful")
        except Exception as e:
            logger.error(f"Firestore connection error: {str(e)}")
            raise

    def create_user(self, user_data):
        """Create a new user document"""
        try:
            doc_ref = self.db.collection('users').document(user_data['username'])
            doc_ref.set({
                'username': user_data['username'],
                'email': user_data['email'],
                'date_joined': firestore.SERVER_TIMESTAMP,
                'credits': 0,
                'is_active': True
            })
            logger.info(f"User created in Firestore: {user_data['username']}")
            return doc_ref
        except Exception as e:
            logger.error(f"Error creating user in Firestore: {str(e)}")
            raise

    def get_user(self, username):
        """Get user document"""
        doc_ref = self.db.collection('users').document(username)
        doc = doc_ref.get()
        return doc.to_dict() if doc.exists else None

    def update_user(self, username, data):
        """Update user document"""
        doc_ref = self.db.collection('users').document(username)
        doc_ref.update(data)

    def create_visa_check(self, check_data):
        """Create visa check record"""
        doc_ref = self.db.collection('visa_checks').document()
        doc_ref.set({
            'user': check_data['user'],
            'from_country': check_data['from_country'],
            'to_country': check_data['to_country'],
            'timestamp': firestore.SERVER_TIMESTAMP,
            'result': check_data['result']
        })
        return doc_ref 