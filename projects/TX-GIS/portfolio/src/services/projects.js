/**
 * Firestore service — portfolio case studies
 *
 * Collection: `projects`
 * Document shape:
 * {
 *   title:        string        — e.g. "City of Waco Utility GIS"
 *   client:       string        — e.g. "City of Waco, TX"
 *   clientType:   string        — "municipality" | "county" | "esd" | "district"
 *   year:         number        — e.g. 2023
 *   services:     string[]      — e.g. ["Utility GIS", "Web Portal"]
 *   summary:      string        — short 1-2 sentence description
 *   description:  string        — full rich description
 *   outcomes:     string[]      — bullet-point outcomes
 *   imageUrl:     string|null   — Firebase Storage URL for hero image
 *   imageUrls:    string[]      — additional project images
 *   demoUrl:      string|null   — relative or absolute URL to live demo (e.g. "../parcel_demo/parcel_map.html")
 *   demoLabel:    string|null   — optional button label override (default: "Live Demo")
 *   featured:     boolean       — show on landing page
 *   order:        number        — display sort order
 *   createdAt:    Timestamp
 *   updatedAt:    Timestamp
 * }
 */

import {
  collection, doc,
  addDoc, updateDoc, deleteDoc,
  getDocs, getDoc,
  query, orderBy, where,
  serverTimestamp,
} from 'firebase/firestore';
import { db } from '../firebase';

const COL = 'projects';
const ref = () => collection(db, COL);

// ── READ ────────────────────────────────────────────

/** Fetch all projects sorted by order */
export async function getProjects() {
  const q = query(ref(), orderBy('order', 'asc'));
  const snap = await getDocs(q);
  return snap.docs.map(d => ({ id: d.id, ...d.data() }));
}

/** Fetch only featured projects */
export async function getFeaturedProjects() {
  const q = query(ref(), where('featured', '==', true), orderBy('order', 'asc'));
  const snap = await getDocs(q);
  return snap.docs.map(d => ({ id: d.id, ...d.data() }));
}

/** Fetch a single project by ID */
export async function getProject(id) {
  const snap = await getDoc(doc(db, COL, id));
  if (!snap.exists()) return null;
  return { id: snap.id, ...snap.data() };
}

// ── WRITE ───────────────────────────────────────────

/** Create a new project */
export async function createProject(data) {
  return addDoc(ref(), {
    ...data,
    featured:  data.featured  ?? false,
    order:     data.order     ?? 0,
    imageUrls: data.imageUrls ?? [],
    services:  data.services  ?? [],
    outcomes:  data.outcomes  ?? [],
    createdAt: serverTimestamp(),
    updatedAt: serverTimestamp(),
  });
}

/** Update an existing project */
export async function updateProject(id, data) {
  return updateDoc(doc(db, COL, id), {
    ...data,
    updatedAt: serverTimestamp(),
  });
}

/** Delete a project */
export async function deleteProject(id) {
  return deleteDoc(doc(db, COL, id));
}
