import type { Metadata } from "next";
import { Barlow_Condensed, IBM_Plex_Mono, Inter } from "next/font/google";
import "./globals.css";

const barlow = Barlow_Condensed({
  variable: "--font-head",
  subsets: ["latin"],
  weight: ["600", "700", "800"],
});

const ibmMono = IBM_Plex_Mono({
  variable: "--font-mono",
  subsets: ["latin"],
  weight: ["400", "500"],
});

const inter = Inter({
  variable: "--font-body",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
});

const BASE_URL = "https://subtxtpress.github.io/home/cases/tiera-strand";

export const metadata: Metadata = {
  metadataBase: new URL(BASE_URL),
  title: "Tiera Strand — Investigative Timeline",
  description:
    "An investigative timeline of the disappearance and death of Tiera Strand, 25, last seen April 16, 2023 on Austin's 6th Street. Body recovered in Bell County, TX. Case active.",
  icons: {
    icon: [
      { url: "/icons/icon-32.png", sizes: "32x32", type: "image/png" },
      { url: "/icons/icon-16.png", sizes: "16x16", type: "image/png" },
    ],
    apple: { url: "/icons/icon-180.png", sizes: "180x180" },
    shortcut: "/icons/favicon.ico",
    other: { rel: "manifest", url: "/icons/site.webmanifest" },
  },
  openGraph: {
    siteName: "Subtxt Press",
    title: "Tiera Strand — Investigative Timeline",
    description:
      "Last seen April 16, 2023 on Austin's 6th Street. Body found in a Bell County ditch, 75 miles away. This case is unsolved.",
    url: BASE_URL,
    type: "website",
    images: [{ url: `${BASE_URL}/tiera-strand.jpg`, width: 1200, height: 675 }],
  },
  twitter: {
    card: "summary_large_image",
    site: "@subtxtpress",
    creator: "@subtxtpress",
    title: "Tiera Strand — Investigative Timeline",
    description:
      "Last seen April 16, 2023 on Austin's 6th Street. Body found in a Bell County ditch, 75 miles away. This case is unsolved.",
    images: [`${BASE_URL}/tiera-strand.jpg`],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${barlow.variable} ${ibmMono.variable} ${inter.variable}`}
    >
      <body>{children}</body>
    </html>
  );
}
