'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';
import styles from './styles.module.css';
import LoginForm from './components/LoginForm';
import SignupForm from './components/SignupForm';
import { authAPI } from '@/services/api';

// Configure axios to handle cookies
axios.defaults.withCredentials = true;

export default function Home() {
  const router = useRouter();
  const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;
  const [isLogin, setIsLogin] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isVerifying, setIsVerifying] = useState(true);

  useEffect(() => {
    const verifyToken = async () => {
      const token = localStorage.getItem('token');
      if (!token) {
        setIsVerifying(false);
        return;
      }

      try {
        await axios.get(`${baseUrl}/`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
          withCredentials: true,
        });
        router.push('/dashboard');
      } catch (err) {
        localStorage.removeItem('token');
        setIsVerifying(false);
      }
    };

    verifyToken();
  }, []);

  const handleLogin = async (username: string, password: string ) => {
    try {
      setError("");
      const response = await authAPI.login(
        username,
        password
      );

      if (response.data.token) {
        localStorage.setItem('token', response.data.token);
        router.push('/dashboard');
      }
    } catch (err: any) {
      setError(err.response?.data?.message || err.response?.data?.error || "An error occurred");
    }
  };

  const handleSignup = async (username: string, email: string, password: string) => {
    try {
      setError("");
      const response = await authAPI.signup(
        username,
        email,
        password
      );

      if (response.data.token) {
        localStorage.setItem('token', response.data.token);
        router.push('/dashboard');
      }
    } catch (err: any) {
      setError(err.response?.data?.message || err.response?.data?.error || "An error occurred");
    }
  };

  if (isVerifying) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>Verifying...</div>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <div className={styles.authContainer}>
        {error && (
          <div
            style={{ color: 'red', textAlign: 'center', marginBottom: '1rem' }}>
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
                onClick={() => setIsLogin(false)}>
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
                onClick={() => setIsLogin(true)}>
                Login
              </button>
            </p>
          </>
        )}
      </div>
    </div>
  );
}
