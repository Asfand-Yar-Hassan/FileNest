"use client"

import React from 'react';
import styles from '../styles.module.css';

interface SignupFormData {
  username: string;
  email: string;
  password: string;
}

interface SignupFormProps {
  onSubmit: (data: SignupFormData) => Promise<void>;
}

export default function SignupForm({ onSubmit }: SignupFormProps) {
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const form = e.currentTarget;
    const formData = new FormData(form);
    
    await onSubmit({
      username: formData.get('username') as string,
      email: formData.get('email') as string,
      password: formData.get('password') as string
    });
  };

  return (
    <form onSubmit={handleSubmit} className={styles.form}>
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
          type="email"
          name="email"
          placeholder="Email"
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
        Sign Up
      </button>
    </form>
  );
} 