import React, {useState} from 'react';
import {AlertCircle, CheckCircle, ChefHat, Mail, X, Lock} from 'lucide-react';
import {Button} from "@/app/components/ui/button";
import "./popup.css"
import { useRouter } from 'next/navigation';

interface AnmeldenProps {
    isOpen: boolean;
    onClose: () => void;
    onSwitchToRegister: () => void;
}

export function Anmelden({ isOpen, onClose, onSwitchToRegister }: AnmeldenProps) {
    const router = useRouter();

    const [formData, setFormData] = useState({
        email: '',
        password: '',
    });

    const [errors, setErrors] = useState({
        email: '',
        password: ''
    });
    const [touched, setTouched] = useState({
        email: false,
        password: false,
    });
    const [message, setMessage] = useState('');

    const validateEmail = (email: string) => {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    };

    // Passwort-Validierung
    const validatePassword = (password: string) => {
        return {
            length: password.length >= 8,
            uppercase: /[A-Z]/.test(password),
            lowercase: /[a-z]/.test(password),
            number: /[0-9]/.test(password),
            special: /[!@#$%^&*(),.?":{}|<>]/.test(password)
        };
    };

    // Alle Validierungen durchführen
    const validate = () => {
        const newErrors = {
            email: '',
            password: '',
        };

        if (!formData.email) {
            newErrors.email = 'E-Mail ist erforderlich';
        } else if (!validateEmail(formData.email)) {
            newErrors.email = 'Ungültige E-Mail-Adresse';
        }

        if (!formData.password) {
            newErrors.password = 'Passwort ist erforderlich';
        } else {
            const checks = validatePassword(formData.password);
            if (!checks.length) {
                newErrors.password = 'Passwort muss mindestens 8 Zeichen lang sein';
            } else if (!checks.uppercase || !checks.lowercase) {
                newErrors.password = 'Passwort muss Groß- und Kleinbuchstaben enthalten';
            } else if (!checks.number) {
                newErrors.password = 'Passwort muss mindestens eine Zahl enthalten';
            } else if (!checks.special) {
                newErrors.password = 'Passwort muss mindestens ein Sonderzeichen enthalten';
            }
        }

        return newErrors;
    };

    const handleChange = (e: { target: { name: any; value: any; }; }) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleBlur = (e: { target: { name: any; }; }) => {
        const { name } = e.target;
        setTouched(prev => ({
            ...prev,
            [name]: true
        }));

        // Validierung beim Verlassen des Feldes
        const newErrors = validate();
        setErrors(newErrors);
    };

    const handleSubmit = async () => {
        // Alle Felder als berührt markieren
        setTouched({
            email: true,
            password: true,
        });

        const newErrors = validate();
        setErrors(newErrors);

        if (!newErrors.email && !newErrors.password) {
            console.log('Formular erfolgreich validiert:', formData);
            try {
                const response = await fetch('http://localhost:3000/api/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData),
                });

                const data = await response.json();


                if (response.ok && data.message.includes('erfolgreich')) {
                    setMessage(data.message || 'Anmeldung erfolgreich');
                    setFormData({ email: '', password: ''});

                    setTouched({email: false, password: false});
                    onClose();
                    setMessage('');
                    router.push('/recipeFinder');

                } else {
                    // Fehler vom Backend (Status 400-599)
                    setMessage(data.detail || data.message || 'Anmeldung fehlgeschlagen');
                }
            } catch (error) {
                // Netzwerkfehler
                setMessage('Netzwerkfehler: Backend nicht erreichbar');
                console.error('Error:', error);
            }
        }
    };

    const handleSwitchToLogin = () => {
        setFormData({
            email: '',
            password: '',
        });

        setErrors({ email: '', password: ''});
        onSwitchToRegister();
    };

    const passwordChecks = validatePassword(formData.password);

    if (!isOpen) return null;

    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <Button
                    className="modal-close"
                    onClick={onClose}
                    aria-label="Schließen"
                >
                    <X className="modal-close-icon" />
                </Button>

                <div className="modal-header">
                    <ChefHat className="modal-icon" />
                    <h2 className="modal-title">Anmelden</h2>
                    <p className="modal-subtitle">
                        Melden Sie sich mit Ihrem Konto an
                    </p>
                </div>

                {message && (
                    <div className={`mt-4 p-3 rounded-md ${
                        message.includes('erfolgreich')
                            ? 'bg-green-100 text-green-700'
                            : 'bg-red-100 text-red-700'
                    }`}>
                        {message}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-5">
                    {/* E-Mail Feld */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            E-Mail
                        </label>
                        <div className="relative">
                            <Mail className="absolute left-3 top-3 text-gray-400" size={20} />
                            <input
                                type="email"
                                name="email"
                                value={formData.email}
                                onChange={handleChange}
                                onBlur={handleBlur}
                                className={`w-full pl-10 pr-4 py-3 border rounded-lg focus:outline-none focus:ring-2 ${
                                    errors.email && touched.email
                                        ? 'border-red-300 focus:ring-red-200'
                                        : 'border-gray-300 focus:ring-blue-200'
                                }`}
                                placeholder="max@beispiel.de"
                            />
                        </div>
                        {errors.email && touched.email && (
                            <p className="mt-1 text-sm text-red-600 flex items-center gap-1">
                                <AlertCircle size={14} />
                                {errors.email}
                            </p>
                        )}
                    </div>

                    {/* Passwort Feld */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Passwort
                        </label>
                        <div className="relative">
                            <Lock className="absolute left-3 top-3 text-gray-400" size={20} />
                            <input
                                type="password"
                                name="password"
                                value={formData.password}
                                onChange={handleChange}
                                onBlur={handleBlur}
                                className={`w-full pl-10 pr-4 py-3 border rounded-lg focus:outline-none focus:ring-2 ${
                                    errors.password && touched.password
                                        ? 'border-red-300 focus:ring-red-200'
                                        : 'border-gray-300 focus:ring-blue-200'
                                }`}
                                placeholder="••••••••"
                            />
                        </div>
                        {errors.password && touched.password && (
                            <p className="mt-1 text-sm text-red-600 flex items-center gap-1">
                                <AlertCircle size={14} />
                                {errors.password}
                            </p>
                        )}

                        {/* Passwort-Stärke Anzeige */}
                        {formData.password && (
                            <div className="mt-3 space-y-2">
                                <p className="text-xs font-medium text-gray-700">Passwort-Anforderungen:</p>
                                <div className="space-y-1">
                                    <PasswordCheck met={passwordChecks.length} text="Mindestens 8 Zeichen" />
                                    <PasswordCheck met={passwordChecks.uppercase && passwordChecks.lowercase} text="Groß- und Kleinbuchstaben" />
                                    <PasswordCheck met={passwordChecks.number} text="Mindestens eine Zahl" />
                                    <PasswordCheck met={passwordChecks.special} text="Mindestens ein Sonderzeichen" />
                                </div>
                            </div>
                        )}
                    </div>

                    <Button
                        onClick={handleSubmit}
                        type="button"
                        className="form-submit"
                    >
                        Anmelden
                    </Button>
                </form>

                <p className="mt-6 text-center text-sm text-gray-600">
                    Noch kein Konto?{' '}
                    <Button
                        type="button"
                        className="form-link"
                        onClick={handleSwitchToLogin}
                    >
                        Jetzt registrieren
                    </Button>
                </p>
            </div>
        </div>
    );
}

// @ts-ignore
function PasswordCheck({met, text }) {
    return (
        <div className="flex items-center gap-2">
            <div className={`w-4 h-4 rounded-full flex items-center justify-center ${
                met ? 'bg-green-500' : 'bg-gray-300'
            }`}>
                {met && <CheckCircle size={12} className="text-white" />}
            </div>
            <span className={`text-xs ${met ? 'text-green-700' : 'text-gray-600'}`}>
        {text}
      </span>
        </div>
    );
}