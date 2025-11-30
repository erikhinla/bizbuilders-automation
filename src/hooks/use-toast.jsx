import { useState, useCallback, createContext, useContext, useEffect } from 'react';

// Toast Context
const ToastContext = createContext(null);

// Toast Provider Component
export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);

  const toast = useCallback(({ title, description, variant = 'default', className = '' }) => {
    const id = Date.now().toString() + Math.random().toString(36).substr(2, 9);
    const newToast = {
      id,
      title,
      description,
      variant,
      className,
    };

    setToasts((prev) => [...prev, newToast]);

    // Auto remove after 3 seconds
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 3000);

    return { id };
  }, []);

  return (
    <ToastContext.Provider value={{ toast, toasts }}>
      {children}
      <Toaster toasts={toasts} />
    </ToastContext.Provider>
  );
}

// Hook to use toast
export function useToast() {
  const context = useContext(ToastContext);
  if (!context) {
    // Fallback if context is not available
    return {
      toast: ({ title, description, variant, className }) => {
        console.log('Toast (no context):', { title, description, variant, className });
        return { id: Date.now().toString() };
      },
      toasts: []
    };
  }
  return context;
}

/**
 * Toast component to display toasts
 */
function Toaster({ toasts }) {
  if (!toasts || toasts.length === 0) return null;

  return (
    <div className="fixed top-4 right-4 z-[100] flex flex-col gap-2">
      {toasts.map((toast) => (
        <div
          key={toast.id}
          className={`
            px-4 py-3 rounded-lg shadow-lg border min-w-[300px] max-w-md
            ${toast.variant === 'destructive' 
              ? 'bg-red-500/90 text-white border-red-600' 
              : toast.className || 'bg-slate-900 text-white border-slate-700'
            }
            animate-in slide-in-from-top-5
          `}
        >
          {toast.title && (
            <div className="font-semibold text-sm">{toast.title}</div>
          )}
          {toast.description && (
            <div className="text-xs mt-1 opacity-90">{toast.description}</div>
          )}
        </div>
      ))}
    </div>
  );
}

export { Toaster };
