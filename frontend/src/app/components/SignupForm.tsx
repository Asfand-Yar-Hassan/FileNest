"use client"

import { useState } from 'react';
import styles from '../styles.module.css';

interface SignupFormProps {
  onSubmit: (
    email: string,
    username: string,
    password: string,
    confirmPassword: string
  ) => void;
}

export default function SignupForm({ onSubmit }: SignupFormProps) {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(email, username, password, confirmPassword);
  };

  return (
    <form onSubmit={handleSubmit} className={styles.authForm}>
      <h2>Sign Up</h2>
      <div className={styles.formGroup}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className={styles.input}
        />
      </div>
      <div className={styles.formGroup}>
        <input
        type='text'
        placeholder='Username'
        value={username}
        onChange={(e)=>setUsername(e.target.value)}
        required
        className={styles.input}/>
      </div>
      <div className={styles.formGroup}>
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          className={styles.input}
        />
      </div>
      <div className={styles.formGroup}>
        <input
          type="password"
          placeholder="Confirm Password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
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