import React, { useState, useEffect } from 'react';
import backgroundImage from '../assets/login_bg.png'; // Update this path as needed

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [emailError, setEmailError] = useState('');

    // Apply background to the body when component mounts
    useEffect(() => {
        // Save original body style
        const originalStyle = {
            backgroundImage: document.body.style.backgroundImage,
            backgroundSize: document.body.style.backgroundSize,
            backgroundPosition: document.body.style.backgroundPosition,
            backgroundRepeat: document.body.style.backgroundRepeat
        };
        
        // Set background image on body
        document.body.style.backgroundImage = `url(${backgroundImage})`;
        document.body.style.backgroundSize = 'cover';
        document.body.style.backgroundPosition = 'center';
        document.body.style.backgroundRepeat = 'no-repeat';
        document.body.style.minHeight = '100vh';
        
        // Clean up function
        return () => {
            document.body.style.backgroundImage = originalStyle.backgroundImage;
            document.body.style.backgroundSize = originalStyle.backgroundSize;
            document.body.style.backgroundPosition = originalStyle.backgroundPosition;
            document.body.style.backgroundRepeat = originalStyle.backgroundRepeat;
        };
    }, []);

    const validateEmail = (email) => {
        const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        return emailRegex.test(email);
    };

    const validatePassword = (password) => {
        const hasUppercase = /[A-Z]/.test(password);
        const hasLowercase = /[a-z]/.test(password);
        const hasNumber = /[0-9]/.test(password);
        const hasSpecialChar = /[^A-Za-z0-9]/.test(password);

        if (!hasUppercase) {
            return 'Password must contain at least one uppercase letter.';
        }
        if (!hasLowercase) {
            return 'Password must contain at least one lowercase letter.';
        }
        if (!hasNumber) {
            return 'Password must contain at least one number.';
        }
        if (hasSpecialChar) {
            return 'Password must not contain special characters.';
        }
        return '';
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        
        // Validate email
        if (!email) {
            setEmailError('Email is required.');
            return;
        }
        
        if (!validateEmail(email)) {
            setEmailError('Please enter a valid email address.');
            return;
        } else {
            setEmailError('');
        }
        
        // Validate password
        const validationError = validatePassword(password);
        if (validationError) {
            setError(validationError);
            return;
        } else {
            setError('');
        }
        
        // If all validations pass
        console.log('Email:', email);
        console.log('Password:', password);
        alert('Login successful!');
    };

    return (
        <main className="login-wrapper" style={styles.mainWrapper}>
            <section className="login-container" style={styles.formContainer}>
                <header>
                    <h1 id="login-heading">Login</h1>
                </header>
                
                <form 
                    onSubmit={handleSubmit} 
                    style={styles.form}
                    aria-labelledby="login-heading"
                    noValidate
                >
                    <fieldset style={styles.fieldset}>
                        <legend className="visually-hidden">Login Information</legend>
                        
                        <div style={styles.inputGroup} role="group">
                            <label 
                                id="email-label" 
                                htmlFor="email"
                                style={styles.label}
                            >
                                Email:
                            </label>
                            <input
                                type="email"
                                id="email"
                                name="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                                aria-required="true"
                                aria-invalid={emailError ? "true" : "false"}
                                aria-labelledby="email-label"
                                aria-describedby={emailError ? "email-error" : undefined}
                                style={styles.input}
                            />
                            {emailError && (
                                <div 
                                    id="email-error" 
                                    role="alert" 
                                    aria-live="assertive"
                                    style={styles.error}
                                >
                                    {emailError}
                                </div>
                            )}
                        </div>
                        
                        <div style={styles.inputGroup} role="group">
                            <label 
                                id="password-label" 
                                htmlFor="password"
                                style={styles.label}
                            >
                                Password:
                            </label>
                            <input
                                type="password"
                                id="password"
                                name="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                                aria-required="true"
                                aria-invalid={error ? "true" : "false"}
                                aria-describedby={error ? "password-error" : undefined}
                                aria-labelledby="password-label"
                                style={styles.input}
                            />
                            {error && (
                                <div 
                                    id="password-error" 
                                    role="alert" 
                                    aria-live="assertive"
                                    style={styles.error}
                                >
                                    {error}
                                </div>
                            )}
                        </div>
                    </fieldset>
                    
                    <div style={styles.formActions}>
                        <button 
                            type="submit" 
                            style={styles.button}
                            aria-label="Log in to your account"
                        >
                            Login
                        </button>
                    </div>
                </form>
            </section>
        </main>
    );
};

const styles = {
    mainWrapper: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
        padding: '20px',
        width:"600px"
    },
    formContainer: {
        maxWidth: '800px',
        width: '100%',
        backgroundColor: 'rgba(255, 255, 255, 0.9)',
        borderRadius: '8px',
        boxShadow: '0 2px 8px rgba(0, 0, 0, 0.2)',
        padding: '20px',
    },
    form: {
        display: 'flex',
        flexDirection: 'column',
    },
    fieldset: {
        border: 'none',
        padding: 0,
        margin: 0,
    },
    inputGroup: {
        marginBottom: '20px',
        textAlign: 'left',
    },
    label: {
        display: 'block',
        marginBottom: '6px',
        fontWeight: 'bold',
        fontSize: '14px',
    },
    input: {
        width: '100%',
        padding: '12px',
        border: '1px solid #ccc',
        borderRadius: '4px',
        fontSize: '16px',
        boxSizing: 'border-box',
    },
    error: {
        color: '#d32f2f',
        fontSize: '14px',
        marginTop: '6px',
        backgroundColor: 'rgba(211, 47, 47, 0.1)',
        padding: '8px',
        borderRadius: '4px',
    },
    formActions: {
        marginTop: '20px',
        display: 'flex',
        justifyContent: 'center',
    },
    button: {
        padding: '12px 24px',
        backgroundColor: '#1976d2',
        color: '#fff',
        border: 'none',
        borderRadius: '4px',
        fontSize: '16px',
        cursor: 'pointer',
        transition: 'background-color 0.3s',
    },
    visuallyHidden: {
        border: 0,
        clip: 'rect(0 0 0 0)',
        height: '1px',
        margin: '-1px',
        overflow: 'hidden',
        padding: 0,
        position: 'absolute',
        width: '1px',
    }
};

export default Login;