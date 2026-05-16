/**
 * Firebase Auth service — admin login/logout
 * Uses Email/Password auth (enable in Firebase Console → Authentication)
 */

import {
  signInWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
} from 'firebase/auth';
import { auth } from '../firebase';

export const login  = (email, password) => signInWithEmailAndPassword(auth, email, password);
export const logout = ()                => signOut(auth);

/** Subscribe to auth state — returns unsubscribe fn */
export const onAuth = (cb) => onAuthStateChanged(auth, cb);
