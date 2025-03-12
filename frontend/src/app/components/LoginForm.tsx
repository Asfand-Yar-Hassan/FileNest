"use client"

import { useState } from 'react';
import styles from '../styles.module.css';

interface LoginFormProps {
  onSubmit: (username: string, password: string) => void;
}

export default function LoginForm({ onSubmit }: LoginFormProps) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(username, password);
  };

  return (
    <form onSubmit={handleSubmit} className={styles.authForm}>
      <h2>Login</h2>
      <div className={styles.formGroup}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) =>setUsername(e.target.value)}
          required
          className={styles.input}
        />
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
      <button type="submit" className={styles.button}>
        Login
      </button>
    </form>
  );
} 