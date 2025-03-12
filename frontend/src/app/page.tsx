"use client"

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';
import styles from './styles.module.css';
import LoginForm from './components/LoginForm';
import SignupForm from './components/SignupForm';

export default function Home() {
  const router = useRouter();
  const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;
  const [isLogin, setIsLogin] = useState(true);
  const [error, setError] = useState<string|null>(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      router.push('/dashboard');
    }
  }, []);

  const handleLogin = async (username: string, password: string) => {
    try {
      const response = await axios.post(`${baseUrl}/login`, {
        username,
        password
      });
      
      // Store the token in localStorage
      localStorage.setItem('token', response.data.token);
      
      // Redirect to dashboard
      router.push('/dashboard');
    } catch (err) {
      if (axios.isAxiosError(err)) {
        setError(err.response?.data?.message || 'Login failed');
      } else {
        setError('An unexpected error occurred');
      }
    }
  };

  const handleSignup = async (
    email: string,
    username: string,
    password: string,
    confirmPassword: string
  ) => {
    console.log("password", password)
    console.log("confirmPassword", confirmPassword)
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    try {
      const response = await axios.post(`${baseUrl}/signup`, {
        email,
        password,
        username,
      });

      // Store the token in localStorage
      localStorage.setItem('token', response.data.token);

      // Redirect to dashboard
      router.push('/dashboard');
    } catch (err) {
      if (axios.isAxiosError(err)) {
        setError(err.response?.data?.message || 'Signup failed');
      } else {
        setError('An unexpected error occurred');
      }
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.authContainer}>
        {error && (
          <div style={{ color: 'red', textAlign: 'center', marginBottom: '1rem' }}>
            {error}
          </div>
        )}
        
        {isLogin ? (
          <>
            <LoginForm onSubmit={handleLogin} />
            <p className={styles.toggleText}>
              Don&apos;t have an account?{' '}
              <button
                className={styles.toggleButton}
                onClick={() => setIsLogin(false)}
              >
                Sign up
              </button>
            </p>
          </>
        ) : (
          <>
            <SignupForm onSubmit={handleSignup} />
            <p className={styles.toggleText}>
              Already have an account?{' '}
              <button
                className={styles.toggleButton}
                onClick={() => setIsLogin(true)}
              >
                Login
              </button>
            </p>
          </>
        )}
      </div>
    </div>
  );
}
