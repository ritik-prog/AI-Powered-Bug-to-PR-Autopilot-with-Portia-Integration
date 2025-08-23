import './globals.css';

export const metadata = {
  title: 'Bug‑to‑PR Autopilot',
  description: 'Automated bug reproduction and fix via Portia',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="light" suppressHydrationWarning>
      <body className="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 transition-colors duration-200">
        {children}
      </body>
    </html>
  );
}