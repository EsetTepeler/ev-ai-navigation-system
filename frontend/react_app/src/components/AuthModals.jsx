import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import './AuthModals.css'; // We'll create this or add to modern-styles.css

export const AuthModal = ({ isOpen, onClose, type = 'login', onSwitchType }) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [username, setUsername] = useState('');
    const [loading, setLoading] = useState(false);
    const { login, register } = useAuth();

    if (!isOpen) return null;

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            if (type === 'login') {
                await login(email, password);
                onClose();
            } else {
                await register({ email, password, username });
                onClose();
            }
        } catch (error) {
            // Error is handled in context (toast)
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-modal-overlay" onClick={onClose}>
            <div className="auth-modal" onClick={e => e.stopPropagation()}>
                <button className="auth-close-btn" onClick={onClose}>×</button>

                <h2>{type === 'login' ? 'Giriş Yap' : 'Kayıt Ol'}</h2>

                <form onSubmit={handleSubmit} className="auth-form">
                    {type === 'register' && (
                        <div className="form-group">
                            <label>Kullanıcı Adı</label>
                            <input
                                type="text"
                                value={username}
                                onChange={e => setUsername(e.target.value)}
                                placeholder="Kullanıcı adınız"
                                required
                            />
                        </div>
                    )}

                    <div className="form-group">
                        <label>E-posta</label>
                        <input
                            type="email"
                            value={email}
                            onChange={e => setEmail(e.target.value)}
                            placeholder="ornek@email.com"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Şifre</label>
                        <input
                            type="password"
                            value={password}
                            onChange={e => setPassword(e.target.value)}
                            placeholder="••••••••"
                            required
                        />
                    </div>

                    <button type="submit" className="auth-submit-btn" disabled={loading}>
                        {loading ? 'İşleniyor...' : (type === 'login' ? 'Giriş Yap' : 'Kayıt Ol')}
                    </button>
                </form>

                <div className="auth-footer">
                    <p>
                        {type === 'login' ? "Hesabınız yok mu?" : "Zaten hesabınız var mı?"}
                        <button className="auth-switch-btn" onClick={onSwitchType}>
                            {type === 'login' ? "Kayıt Ol" : "Giriş Yap"}
                        </button>
                    </p>
                </div>
            </div>
        </div>
    );
};
