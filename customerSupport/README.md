graph TD
    A[User Registration Form] --> B[Django Auth System]
    B --> C[User.objects.create_user]
    
    C --> D[Signal: handle_new_user_email]
    D --> E{is_created?}
    
    E -- Yes --> F[EmailManager.__init__]
    E -- No --> Z[End Process]
    
    F --> G[EmailManager.send_welcome_email]
    G --> H[EmailManager.send_email]
    
    H --> I{Template Exists?}
    I -- Yes --> J[Template.render]
    I -- No --> Y[Logger.error]
    
    J --> K[SMTP.connect]
    K --> L{Connection OK?}
    
    L -- Yes --> M[SMTP.send_message]
    L -- No --> X[Logger.error]
    
    M --> N{Send Success?}
    N -- Yes --> O[Logger.info]
    N -- No --> W[Logger.error]
    
    O --> P[SMTP.quit]
    P --> Q[End Process]
    
    W --> Q
    X --> Q
    Y --> Q