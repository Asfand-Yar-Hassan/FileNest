"use client"

import React from 'react';
import styles from '../styles.module.css';

interface LoginFormData {
  username: string;
  password: string;
}

interface LoginFormProps {
  onSubmit: (data: LoginFormData) => Promise<void>;
}

export default function LoginForm({ onSubmit }: LoginFormProps) {
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const form = e.currentTarget;
    const formData = new FormData(form);
    
    await onSubmit({
      username: formData.get('username') as string,
      password: formData.get('password') as string
    });
  };

  return (
    <form onSubmit={handleSubmit} className={styles.form}>
      <h2>Login</h2>
      <div className={styles.formGroup}>
        <input
          type="text"
          name="username"
          placeholder="Username"
          required
          className={styles.input}
        />
      </div>
      <div className={styles.formGroup}>
        <input
          type="password"
          name="password"
          placeholder="Password"
          required
          className={styles.input}
        />
      </div>
      <button type="submit" className={styles.button}>
        Login
      </button>
    </form>
  );
} 