"use client"

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';
import styles from '../styles.module.css';

interface File {
  id: number;
  name: string;
  size: number;
  uploaded_at: string;
}

export default function Dashboard() {
  const router = useRouter();
  const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;
  const [files, setFiles] = useState<File[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/');
      return;
    }
    fetchFiles();
  }, []);

  const fetchFiles = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${baseUrl}/`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      setFiles(response.data.files);
    } catch (err) {
      if (axios.isAxiosError(err)) {
        setError(err.response?.data?.message || 'Failed to fetch files');
      } else {
        setError('An unexpected error occurred');
      }
    }
  };

  const handleDelete = async (fileId: number) => {
    try {
      const token = localStorage.getItem('token');
      await axios.delete(`${baseUrl}/delete_file/`, {
        headers: {
          Authorization: `Bearer ${token}`
        },
        data: { file_id: fileId }
      });
      fetchFiles(); // Refresh the file list
    } catch (err) {
      if (axios.isAxiosError(err)) {
        setError(err.response?.data?.message || 'Failed to delete file');
      } else {
        setError('An unexpected error occurred');
      }
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.dashboardContainer}>
        <h1>Your Files</h1>
        {error && (
          <div style={{ color: 'red', marginBottom: '1rem' }}>
            {error}
          </div>
        )}
        <table className={styles.fileTable}>
          <thead>
            <tr>
              <th>Name</th>
              <th>Size</th>
              <th>Uploaded At</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {files.map((file) => (
              <tr key={file.id}>
                <td>{file.name}</td>
                <td>{Math.round(file.size / 1024)} KB</td>
                <td>{new Date(file.uploaded_at).toLocaleDateString()}</td>
                <td>
                  <button
                    onClick={() => handleDelete(file.id)}
                    className={styles.deleteButton}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
} 