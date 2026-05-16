/**
 * Firebase Storage service — project image uploads
 */

import {
  ref as storageRef,
  uploadBytesResumable,
  getDownloadURL,
  deleteObject,
} from 'firebase/storage';
import { storage } from '../firebase';

/**
 * Upload a project image with progress callback.
 * @param {File}     file       — the file to upload
 * @param {string}   projectId  — used to namespace the path
 * @param {Function} onProgress — called with 0–100 progress number
 * @returns {Promise<string>}   — resolves with the download URL
 */
export function uploadProjectImage(file, projectId, onProgress) {
  return new Promise((resolve, reject) => {
    const ext  = file.name.split('.').pop();
    const path = `projects/${projectId}/${Date.now()}.${ext}`;
    const ref  = storageRef(storage, path);
    const task = uploadBytesResumable(ref, file);

    task.on(
      'state_changed',
      snap => {
        const pct = Math.round((snap.bytesTransferred / snap.totalBytes) * 100);
        onProgress?.(pct);
      },
      reject,
      async () => {
        const url = await getDownloadURL(task.snapshot.ref);
        resolve({ url, path });
      }
    );
  });
}

/**
 * Delete an image by its storage path.
 */
export function deleteProjectImage(path) {
  return deleteObject(storageRef(storage, path));
}
