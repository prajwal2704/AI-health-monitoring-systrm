import React, { useState } from 'react';
import { Heart, Mail, Lock, User, Calendar } from 'lucide-react';
import { loginUser, registerUser } from '../services/api';
import './LoginPage.css';

const LoginPage = ({ onLoginSuccess }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    fullName: '',
    dateOfBirth: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const data = isLogin
        ? await loginUser({ email: formData.email, password: formData.password })
        : await registerUser({
            full_name: formData.fullName,
            date_of_birth: formData.dateOfBirth,
            email: formData.email,
            password: formData.password
          });

      if (data.success) {
        setSuccess(isLogin ? 'Login successful!' : 'Registration successful!');
        localStorage.setItem('session_token', data.session_token);
        localStorage.setItem('user', JSON.stringify(data.user));

        // Call onLoginSuccess after a brief delay to show success message
        setTimeout(() => {
          onLoginSuccess(data.session_token, data.user);
        }, 1000);
      } else {
        setError(data.error || 'An error occurred');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Network error. Please check if the server is running.');
    } finally {
      setLoading(false);
    }
  };

  const toggleMode = () => {
    setIsLogin(!isLogin);
    setError('');
    setSuccess('');
    setFormData({
      email: '',
      password: '',
      fullName: '',
      dateOfBirth: ''
    });
  };

  return (
    <div className="login-page">
      {/* Background Image */}
      <div className="background-image"></div>

      {/* Login Form */}
      <div className="login-container">
        <div className="login-header">
          <div className="logo">
            <Heart size={40} className="heart-icon" />
            <h1>CarePulse</h1>
          </div>
          <p className="tagline">
            Clinical health monitoring and disease prediction portal
          </p>
        </div>

        <div className="login-form-container">
          <div className="form-header">
            <h2>{isLogin ? 'Welcome Back' : 'Create Account'}</h2>
            <p>
              {isLogin
                ? 'Sign in to continue your medical consultations'
                : 'Join us for personalized healthcare assistance'
              }
            </p>
          </div>

          <form onSubmit={handleSubmit} className="login-form">
            {!isLogin && (
              <>
                <div className="form-group">
                  <label htmlFor="fullName">
                    <User size={18} />
                    Full Name
                  </label>
                  <input
                    type="text"
                    id="fullName"
                    name="fullName"
                    value={formData.fullName}
                    onChange={handleInputChange}
                    required={!isLogin}
                    placeholder="Enter your full name"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="dateOfBirth">
                    <Calendar size={18} />
                    Date of Birth
                  </label>
                  <input
                    type="date"
                    id="dateOfBirth"
                    name="dateOfBirth"
                    value={formData.dateOfBirth}
                    onChange={handleInputChange}
                    required={!isLogin}
                  />
                </div>
              </>
            )}

            <div className="form-group">
              <label htmlFor="email">
                <Mail size={18} />
                Email Address
              </label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                required
                placeholder="Enter your email"
                autoComplete="email"
              />
            </div>

            <div className="form-group">
              <label htmlFor="password">
                <Lock size={18} />
                Password
              </label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleInputChange}
                required
                placeholder="Enter your password"
                autoComplete={isLogin ? "current-password" : "new-password"}
              />
            </div>

            {error && (
              <div className="error-message">
                {error}
              </div>
            )}

            {success && (
              <div className="success-message">
                {success}
              </div>
            )}

            <button
              type="submit"
              className="login-button"
              disabled={loading}
            >
              {loading ? (
                <>
                  <div className="spinner"></div>
                  {isLogin ? 'Signing In...' : 'Creating Account...'}
                </>
              ) : (
                isLogin ? 'Sign In' : 'Create Account'
              )}
            </button>
          </form>

          <div className="form-footer">
            <p>
              {isLogin ? "Don't have an account?" : "Already have an account?"}
              <button
                type="button"
                className="toggle-button"
                onClick={toggleMode}
                disabled={loading}
              >
                {isLogin ? 'Sign Up' : 'Sign In'}
              </button>
            </p>
          </div>
        </div>

        <div className="features-preview">
          <div className="feature">
            <div className="feature-icon">🩺</div>
            <span>Clinical Diagnostic Guidance</span>
          </div>
          <div className="feature">
            <div className="feature-icon">🔒</div>
            <span>Secure & Private Consultations</span>
          </div>
          <div className="feature">
            <div className="feature-icon">🌍</div>
            <span>Multi-Language Support</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;

