#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
██████╗██╗  ██╗███████╗██████╗ ██████╗  █████╗ ██╗  ██╗
██╔════╝██║  ██║██╔════╝██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝
██║     ███████║█████╗  ██████╔╝██████╔╝███████║█████╔╝ 
██║     ██╔══██║██╔══╝  ██╔══██╗██╔══██╗██╔══██║██╔═██╗ 
╚██████╗██║  ██║███████╗██║  ██║██║  ██║██║  ██║██║  ██╗
╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
                                                          
   Cherrak Bank AI - V87 Sovereign Ether Core
   Version: 7.8.7 | Architecture: Quantum AI Banking
   Port: 7000
   (c) 2025 Cherrak G7 Group | All Rights Reserved
"""
# ═══════════════════════════════════════════════════════════════════════════════
# CHERRAK BANK AI GLOBAL - V87 ETHER SOVEREIGN
# نظام مصرفي رقمي متطور بالذكاء الاصطناعي | المنفذ: 7000
# ═══════════════════════════════════════════════════════════════════════════════

import os
import json
import uuid
import hashlib
import secrets
import datetime
import time
import random
import string
import smtplib
import threading
from functools import wraps
from flask import Flask, render_template_string, request, session, redirect, url_for, jsonify, make_response, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.middleware.proxy_fix import ProxyFix
import logging
from logging.handlers import RotatingFileHandler

# ============================== التهيئة الأساسية ================================
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "CHERRAK_V87_ETH_SOVEREIGN_9x9x9x_CRYPTO_QUANTUM_PORT_7000")
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False  # ضع True في الإنتاج HTTPS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# ============================== نظام السجلات المتقدم ==============================
if not os.path.exists('logs'):
    os.mkdir('logs')
file_handler = RotatingFileHandler('logs/cherrak_bank.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('Cherrak Bank V87 بدأ التشغيل بنجاح على المنفذ 7000')

# ============================== قاعدة بيانات افتراضية (ذكية) ==============================
# في الإنتاج، استبدل هذا بـ SQLAlchemy + PostgreSQL
users_db = {}          # {username: {hash, salt, mfa_secret, balance, accounts, transactions, etc}}
accounts_db = {}       # {account_id: {user, type, currency, balance, iban}}
transactions_db = []   # list of all transactions
ai_models_db = {       # نماذج ذكاء اصطناعي مسبقة التدريب (شبكات عصبية وهمية)
    'stock_predictor': {'weights': [0.34, 0.56, 0.78, 0.12], 'bias': 0.43},
    'crypto_sentiment': {'level': 'BULLISH', 'confidence': 0.87},
    'risk_score_model': {'thresholds': {'low': 0.3, 'medium': 0.6, 'high': 0.9}}
}

# بيانات تجريبية أولية
def init_demo_users():
    if 'admin' not in users_db:
        users_db['admin'] = {
            'password_hash': generate_password_hash('Admin@007'),
            'full_name': 'مدير النظام - هواري شرق',
            'email': 'admin@cherrakbank.ai',
            'phone': '+213550000000',
            'mfa_enabled': False,
            'mfa_secret': None,
            'accounts': ['CH_ACC_MAIN_001', 'CH_ACC_SAV_002', 'CH_ACC_INV_003'],
            'created_at': datetime.datetime.now().isoformat(),
            'last_login': None,
            'kyc_level': 3,
            'ai_preferences': {'risk_tolerance': 0.65, 'advisor_language': 'ar', 'notify_alerts': True}
        }
    if 'CH_ACC_MAIN_001' not in accounts_db:
        accounts_db['CH_ACC_MAIN_001'] = {
            'user': 'admin',
            'type': 'checking',
            'currency': 'USD',
            'balance': 14285400000.00,  # 14 مليار دولار وهمية
            'iban': 'CR87 0000 0000 0000 0000 0001',
            'created': datetime.datetime.now().isoformat(),
            'is_frozen': False
        }
    if 'CH_ACC_SAV_002' not in accounts_db:
        accounts_db['CH_ACC_SAV_002'] = {
            'user': 'admin',
            'type': 'savings',
            'currency': 'EUR',
            'balance': 250000000.00,
            'iban': 'CR87 0000 0000 0000 0000 0002',
            'created': datetime.datetime.now().isoformat(),
            'interest_rate': 0.025
        }
    if 'CH_ACC_INV_003' not in accounts_db:
        accounts_db['CH_ACC_INV_003'] = {
            'user': 'admin',
            'type': 'investment',
            'currency': 'BTC',
            'balance': 1250.5,
            'iban': 'CR87 0000 0000 0000 0000 0003',
            'created': datetime.datetime.now().isoformat(),
            'crypto_wallet': '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa'
        }
    # إضافة معاملات تجريبية
    for i in range(50):
        transactions_db.append({
            'id': str(uuid.uuid4()),
            'from_account': 'CH_ACC_MAIN_001',
            'to_account': 'CH_ACC_SAV_002' if i%2==0 else 'EXT_BINANCE',
            'amount': round(random.uniform(100, 50000), 2),
            'currency': 'USD',
            'timestamp': (datetime.datetime.now() - datetime.timedelta(days=i)).isoformat(),
            'status': 'completed',
            'type': 'transfer' if i%3 !=0 else 'investment',
            'ai_risk_score': round(random.uniform(0.1, 0.9), 2)
        })
init_demo_users()

# ============================== دوال مساعدة (AI & Utilities) ==============================
def generate_iban():
    """توليد IBAN وهمي فريد"""
    return f"CR87 {random.randint(1000,9999)} {random.randint(1000,9999)} {random.randint(1000,9999)} {random.randint(1000,9999)} {random.randint(1000,9999)}"

def ai_predict_market(symbol='BTC/USD'):
    """محاكاة ذكاء اصطناعي لتوقع السوق"""
    # نموذج تنبؤ بسيط باستخدام مؤشرات افتراضية
    sentiment = random.choice(['BULLISH', 'BEARISH', 'NEUTRAL'])
    confidence = round(random.uniform(0.55, 0.95), 2)
    predicted_price = random.uniform(35000, 75000) if symbol == 'BTC/USD' else random.uniform(2000, 4000)
    recommendation = "شراء" if sentiment == 'BULLISH' else "بيع" if sentiment == 'BEARISH' else "احتفاظ"
    return {
        'symbol': symbol,
        'sentiment': sentiment,
        'confidence': confidence,
        'predicted_price': predicted_price,
        'recommendation': recommendation,
        'timestamp': datetime.datetime.now().isoformat(),
        'model_version': 'V87_Quantum_NeuralNet_2.0'
    }

def ai_risk_assessment(transaction_data):
    """تقييم مخاطر المعاملة باستخدام الذكاء الاصطناعي"""
    amount = transaction_data.get('amount', 0)
    history_factor = min(1.0, len(transactions_db) / 1000)
    risk_score = 0.0
    if amount > 100000:
        risk_score += 0.4
    if amount > 1000000:
        risk_score += 0.3
    if history_factor < 0.1:
        risk_score += 0.2
    # إضافة عشوائية ذكية
    risk_score += random.uniform(-0.05, 0.05)
    risk_score = min(1.0, max(0.0, risk_score))
    decision = "approved" if risk_score < 0.65 else "manual_review" if risk_score < 0.85 else "rejected"
    return {
        'risk_score': round(risk_score, 3),
        'decision': decision,
        'alerts': ['مبلغ كبير غير معتاد'] if amount > 500000 else [],
        'processing_time_ms': random.randint(50, 200)
    }

def ai_financial_advisor(user_id, total_balance):
    """مستشار مالي ذكي يقدم نصائح مخصصة"""
    advice = []
    if total_balance > 1000000:
        advice.append({
            'title': 'فرصة استثمارية ممتازة',
            'description': f'بناءً على تحليل {len(transactions_db)} معاملة سابقة، نقترح تخصيص 30% من رصيدك إلى صندوق Cherrak Growth AI Fund.',
            'priority': 'high',
            'roi_expected': '+12.5% سنويًا'
        })
    else:
        advice.append({
            'title': 'نصيحة للتوفير',
            'description': 'حساب التوفير الذكي يمنحك عائد 4.2% بدون مخاطرة. ابدأ بإيداع 500 دولار شهريًا.',
            'priority': 'medium'
        })
    # تحليل السوق
    market = ai_predict_market('BTC/USD')
    if market['sentiment'] == 'BULLISH':
        advice.append({
            'title': 'توصية تداول العملات الرقمية',
            'description': f"نموذجنا AI V87 يتوقع صعود BTC بنسبة {market['confidence']*100:.0f}%. اقتراح: {market['recommendation']} عند السعر الحالي.",
            'priority': 'medium'
        })
    return {'advice': advice, 'generated_at': datetime.datetime.now().isoformat()}

# ============================== زينة وبينات وهمية للإحصائيات ==============================
def get_live_stats():
    """إحصائيات حية للمنصة"""
    total_assets = sum(acc['balance'] for acc in accounts_db.values())
    return {
        'total_users': len(users_db),
        'total_accounts': len(accounts_db),
        'total_assets_usd': total_assets,
        'daily_transactions': len([t for t in transactions_db if datetime.datetime.fromisoformat(t['timestamp']).date() == datetime.datetime.today().date()]),
        'ai_decision_rate': '94.7%',
        'uptime': '99.999%',
        'last_block': f"V87-{int(time.time())}",
        'network_hash': hashlib.sha256(f"cherrak{time.time()}".encode()).hexdigest()[:16],
        'active_port': '7000'
    }

# ============================== ديكورات الحماية ==============================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'authenticated' not in session:
            flash('الرجاء تسجيل الدخول أولاً', 'warning')
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('username') != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

# ============================== واجهات API للذكاء الاصطناعي ==============================
@app.route('/api/ai/predict', methods=['GET'])
@login_required
def api_ai_predict():
    symbol = request.args.get('symbol', 'BTC/USD')
    return jsonify(ai_predict_market(symbol))

@app.route('/api/ai/risk', methods=['POST'])
@login_required
def api_ai_risk():
    data = request.get_json()
    if not data:
        data = {'amount': request.form.get('amount', 0)}
    return jsonify(ai_risk_assessment(data))

@app.route('/api/ai/advice', methods=['GET'])
@login_required
def api_ai_advice():
    username = session.get('username')
    if not username or username not in users_db:
        return jsonify({'error': 'User not found'}), 404
    total = sum(accounts_db[acc]['balance'] for acc in users_db[username].get('accounts', []) if acc in accounts_db)
    return jsonify(ai_financial_advisor(username, total))

@app.route('/api/transactions', methods=['GET'])
@login_required
def api_transactions():
    """إرجاع معاملات المستخدم بصيغة JSON"""
    username = session.get('username')
    user_accs = users_db.get(username, {}).get('accounts', [])
    user_txs = [tx for tx in transactions_db if tx['from_account'] in user_accs or tx['to_account'] in user_accs]
    return jsonify(user_txs[-50:])  # آخر 50 معاملة

@app.route('/api/account/balance', methods=['GET'])
@login_required
def api_account_balance():
    username = session.get('username')
    acc_id = request.args.get('account_id')
    if username not in users_db:
        return jsonify({'error': 'Unauthorized'}), 401
    if acc_id and acc_id in accounts_db and accounts_db[acc_id]['user'] == username:
        balance = accounts_db[acc_id]['balance']
    else:
        # مجموع جميع الحسابات
        balance = sum(accounts_db[acc]['balance'] for acc in users_db[username].get('accounts', []) if acc in accounts_db)
    return jsonify({'balance': balance, 'currency': 'USD', 'timestamp': datetime.datetime.now().isoformat()})

@app.route('/api/transfer', methods=['POST'])
@login_required
def api_transfer():
    """تحويل أموال بالذكاء الاصطناعي وتقييم المخاطر"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid data'}), 400
    from_acc = data.get('from_account')
    to_acc = data.get('to_account')
    amount = float(data.get('amount', 0))
    if amount <= 0:
        return jsonify({'error': 'Amount must be positive'}), 400
    username = session.get('username')
    if from_acc not in accounts_db or accounts_db[from_acc]['user'] != username:
        return jsonify({'error': 'Invalid source account'}), 403
    if accounts_db[from_acc]['balance'] < amount:
        return jsonify({'error': 'Insufficient funds'}), 400
    
    # تقييم المخاطر بواسطة الذكاء الاصطناعي
    risk = ai_risk_assessment({'amount': amount, 'from': from_acc, 'to': to_acc})
    if risk['decision'] == 'rejected':
        return jsonify({'error': f'Transaction rejected by AI risk engine. Score: {risk["risk_score"]}', 'risk': risk}), 403
    
    # تنفيذ التحويل
    accounts_db[from_acc]['balance'] -= amount
    if to_acc in accounts_db:
        accounts_db[to_acc]['balance'] += amount
    else:
        # حساب خارجي (محاكاة)
        pass
    
    # تسجيل المعاملة
    tx_id = str(uuid.uuid4())
    transaction = {
        'id': tx_id,
        'from_account': from_acc,
        'to_account': to_acc,
        'amount': amount,
        'currency': 'USD',
        'timestamp': datetime.datetime.now().isoformat(),
        'status': 'completed' if risk['decision'] == 'approved' else 'pending_review',
        'type': 'transfer',
        'ai_risk_score': risk['risk_score']
    }
    transactions_db.append(transaction)
    
    # إشعار ذكي (في الواقع إرسال بريد إلكتروني أو WebSocket)
    app.logger.info(f"Transfer {tx_id} from {from_acc} to {to_acc} amount ${amount} risk={risk['risk_score']}")
    
    return jsonify({'success': True, 'transaction_id': tx_id, 'new_balance': accounts_db[from_acc]['balance'], 'risk': risk})

@app.route('/api/stats', methods=['GET'])
@login_required
def api_stats():
    """إحصائيات حية للمنصة"""
    return jsonify(get_live_stats())

@app.route('/api/user/accounts', methods=['GET'])
@login_required
def api_user_accounts():
    username = session.get('username')
    if username not in users_db: return jsonify([])
    user_accounts = []
    for acc_id in users_db[username].get('accounts', []):
        if acc_id in accounts_db:
            user_accounts.append({'id': acc_id, 'type': accounts_db[acc_id]['type'], 'balance': accounts_db[acc_id]['balance'], 'iban': accounts_db[acc_id]['iban']})
    return jsonify(user_accounts)

# ============================== واجهات المستخدم الرئيسية ==============================
HTML_MAIN = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <title>Cherrak AI Bank | V87 Sovereign Core | Port 7000</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,500;14..32,700;14..32,900&family=Cairo:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: radial-gradient(circle at 20% 30%, #0a0f1e, #03050b);
            font-family: 'Cairo', 'Inter', sans-serif;
            color: #eef5ff;
            min-height: 100vh;
            padding: 20px;
        }
        .glass-panel {
            background: rgba(15, 25, 45, 0.55);
            backdrop-filter: blur(14px);
            border: 1px solid rgba(0, 255, 255, 0.2);
            border-radius: 2rem;
            box-shadow: 0 20px 40px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05);
        }
        .neon-text {
            text-shadow: 0 0 5px #0ff, 0 0 10px #0ff;
            color: #ccf3ff;
        }
        .ai-badge {
            background: linear-gradient(135deg, #00c6ff, #0072ff);
            border-radius: 60px;
            padding: 6px 14px;
            font-size: 0.7rem;
            font-weight: bold;
        }
        button {
            transition: all 0.2s ease;
            cursor: pointer;
        }
        button:active { transform: scale(0.97); }
        .card-stats {
            background: rgba(0,0,0,0.5);
            border-radius: 1.5rem;
            padding: 1.2rem;
            border-left: 4px solid #0ff;
        }
        .transfer-form input, .transfer-form select {
            background: #0f172a;
            border: 1px solid #334155;
            border-radius: 1rem;
            padding: 0.8rem;
            color: white;
        }
        .transaction-item {
            background: rgba(255,255,255,0.03);
            margin: 0.5rem 0;
            padding: 0.8rem;
            border-radius: 1rem;
            display: flex;
            justify-content: space-between;
            font-family: monospace;
        }
        @keyframes pulse {
            0% { opacity: 0.6; }
            100% { opacity: 1; }
        }
        .live-badge {
            background: #ff3366;
            border-radius: 20px;
            padding: 3px 10px;
            font-size: 0.7rem;
            animation: pulse 1s infinite;
        }
        .port-badge {
            background: #00ff88;
            color: #000;
            border-radius: 20px;
            padding: 3px 10px;
            font-size: 0.7rem;
            font-weight: bold;
        }
        @media (max-width: 768px) {
            body { padding: 10px; }
            .grid-cols-2 { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
<div class="max-w-7xl mx-auto">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6 flex-wrap gap-3">
        <div>
            <h1 class="text-3xl font-black"><span class="neon-text">CHERRAK</span> <span class="text-cyan-300">AI BANK</span> <span class="text-xs bg-purple-700/60 rounded-full px-3 py-1">V87 Sovereign Ether</span></h1>
            <p class="text-gray-400 text-sm">المنصة المصرفية بالذكاء الاصطناعي التوليدي المتقدم | المنفذ: 7000</p>
        </div>
        <div class="flex gap-3">
            <div class="glass-panel px-4 py-2 flex gap-2 items-center"><i class="fa-solid fa-microchip text-green-400"></i> <span id="ai-status">AI Online</span></div>
            <div class="port-badge px-4 py-2 flex gap-2 items-center"><i class="fa-solid fa-plug"></i> PORT: 7000</div>
            <button onclick="location.href='/logout'" class="bg-red-500/20 border border-red-500 rounded-full px-5 py-2 hover:bg-red-500/40"><i class="fa-solid fa-lock"></i> خروج</button>
        </div>
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <!-- البطاقة الرئيسية للرصيد -->
        <div class="lg:col-span-2 glass-panel p-6">
            <div class="flex justify-between items-start">
                <div><span class="text-gray-400 text-sm">الرصيد الإجمالي</span>
                    <h2 class="text-4xl md:text-5xl font-black tracking-tighter" id="total-balance">$0.00</h2>
                    <span class="text-xs text-green-300"><i class="fa-regular fa-clock"></i> محدث بشكل لحظي</span>
                </div>
                <div class="ai-badge"><i class="fa-regular fa-brain"></i> AI Advisor Active</div>
            </div>
            <div class="mt-4 flex gap-3 flex-wrap">
                <select id="account-selector" class="bg-black/40 border border-cyan-500 rounded-xl p-2 text-sm">
                    <option value="all">جميع الحسابات</option>
                </select>
                <button onclick="refreshBalance()" class="bg-cyan-600 px-4 rounded-xl"><i class="fa-solid fa-rotate"></i> تحديث</button>
            </div>
        </div>
        <!-- إحصائيات سريعة من AI -->
        <div class="glass-panel p-5">
            <div class="flex justify-between"><span><i class="fa-regular fa-chart-line"></i> مؤشر السوق AI</span> <span class="live-badge">LIVE</span></div>
            <div id="ai-market-prediction" class="mt-2 text-lg font-bold">تحميل التوقعات...</div>
            <div class="text-xs text-gray-400 mt-2" id="ai-conf">الثقة: --%</div>
            <div class="h-1 bg-gray-700 mt-3 rounded-full"><div class="h-1 bg-cyan-400 rounded-full" style="width: 87%"></div></div>
            <div class="mt-3 text-center"><i class="fa-regular fa-message"></i> <span id="ai-recom">توصية</span></div>
        </div>
    </div>

    <!-- منطقة عمل رئيسية: تحويل + معاملات -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-7">
        <!-- قسم التحويل المحمي بالذكاء الاصطناعي -->
        <div class="glass-panel p-6">
            <h3 class="text-xl font-bold mb-4"><i class="fa-regular fa-paper-plane"></i> تحويل فوري بتقييم المخاطر الذكي</h3>
            <div class="transfer-form space-y-4">
                <select id="from-acc" class="w-full">
                    <option value="">من حساب</option>
                </select>
                <input type="text" id="to-acc" placeholder="رقم الحساب أو IBAN الوجهة" class="w-full">
                <input type="number" id="amount" placeholder="المبلغ بالدولار" class="w-full">
                <button id="transfer-btn" class="w-full bg-gradient-to-r from-cyan-600 to-blue-700 rounded-xl p-3 font-bold"><i class="fa-regular fa-shield"></i> تقييم وتنفيذ التحويل</button>
                <div id="risk-output" class="text-xs text-yellow-300"></div>
            </div>
        </div>

        <!-- نصائح المستشار المالي AI -->
        <div class="glass-panel p-6">
            <h3 class="text-xl font-bold mb-3"><i class="fa-regular fa-robot"></i> مستشار Cherrak المالي AI</h3>
            <div id="ai-advice-container" class="space-y-3">
                <div class="animate-pulse">جاري تحليل بيانات السوق العالمية...</div>
            </div>
            <button onclick="loadAIAdvice()" class="mt-3 text-cyan-400 text-sm"><i class="fa-regular fa-arrows-rotate"></i> تحديث التوصيات</button>
        </div>
    </div>

    <!-- سجل المعاملات والرسوم البيانية -->
    <div class="mt-8 glass-panel p-6">
        <div class="flex justify-between items-center flex-wrap"><h3 class="font-bold text-xl"><i class="fa-regular fa-list-timeline"></i> المعاملات الأخيرة (مشفرة على الـ Blockchain الداخلي)</h3><span class="text-xs text-gray-400">آخر 50 حركة</span></div>
        <div class="h-48 mt-3"><canvas id="txChart"></canvas></div>
        <div id="transactions-list" class="max-h-64 overflow-y-auto mt-4 space-y-2">
            <div class="text-center text-gray-500">تحميل المعاملات...</div>
        </div>
    </div>
</div>

<script>
    let chartInstance = null;
    async function fetchJSON(endpoint) {
        const res = await fetch(endpoint);
        if(!res.ok) throw new Error(await res.text());
        return res.json();
    }
    async function refreshBalance() {
        try {
            let data = await fetchJSON('/api/account/balance');
            document.getElementById('total-balance').innerHTML = '$ ' + data.balance.toLocaleString('en-US', {minimumFractionDigits:2});
        } catch(e) { console.error(e); }
    }
    async function loadTransactions() {
        try {
            const txs = await fetchJSON('/api/transactions');
            const container = document.getElementById('transactions-list');
            if(txs.length===0) container.innerHTML = '<div class="text-center text-gray-500">لا توجد معاملات</div>';
            else {
                container.innerHTML = txs.map(tx => `<div class="transaction-item"><span><i class="fa-regular fa-arrow-right-arrow-left"></i> ${tx.from_account} → ${tx.to_account}</span><span class="text-cyan-300">$${tx.amount.toLocaleString()}</span><span class="text-xs text-gray-400">${new Date(tx.timestamp).toLocaleString()}</span></div>`).join('');
            }
            // رسم بياني بسيط
            const amounts = txs.slice(0,10).map(t=>t.amount);
            const ctx = document.getElementById('txChart').getContext('2d');
            if(chartInstance) chartInstance.destroy();
            chartInstance = new Chart(ctx, { type: 'line', data: { labels: amounts.map((_,i)=>i+1), datasets: [{ label: 'قيمة التحويلات (USD)', data: amounts, borderColor: '#0ff', tension:0.3 }] } });
        } catch(e) { console.error(e); }
    }
    async function loadAIPrediction() {
        try {
            const pred = await fetchJSON('/api/ai/predict?symbol=BTC/USD');
            document.getElementById('ai-market-prediction').innerHTML = `BTC/USD: ${pred.sentiment} → ${pred.recommendation}`;
            document.getElementById('ai-conf').innerHTML = `الثقة: ${(pred.confidence*100).toFixed(0)}% | السعر المتوقع: $${pred.predicted_price.toFixed(0)}`;
            document.getElementById('ai-recom').innerHTML = pred.recommendation;
        } catch(e) {console.error(e);}
    }
    async function loadAIAdvice() {
        try {
            const advice = await fetchJSON('/api/ai/advice');
            const container = document.getElementById('ai-advice-container');
            if(advice.advice && advice.advice.length) {
                container.innerHTML = advice.advice.map(a => `<div class="border border-cyan-800/40 rounded-xl p-3"><strong>💡 ${a.title}</strong><p class="text-sm text-gray-300">${a.description}</p>${a.roi_expected ? `<span class="text-green-400 text-xs">${a.roi_expected}</span>` : ''}</div>`).join('');
            } else container.innerHTML = '<div class="text-gray-400">لا توجد نصائح جديدة</div>';
        } catch(e) { container.innerHTML = '<div class="text-red-400">خطأ في الاتصال بالمستشار</div>'; }
    }
    async function loadAccounts() {
        try {
            const accs = await fetchJSON('/api/user/accounts');
            const selectFrom = document.getElementById('from-acc');
            const selectAcc = document.getElementById('account-selector');
            if(selectFrom) {
                selectFrom.innerHTML = '<option value="">اختر حساب</option>';
                accs.forEach(acc => {
                    selectFrom.innerHTML += `<option value="${acc.id}">${acc.type} - ${acc.iban} (${acc.balance} ${acc.currency || 'USD'})</option>`;
                });
            }
            if(selectAcc) {
                selectAcc.innerHTML = '<option value="all">كل الحسابات</option>';
                accs.forEach(acc => {
                    selectAcc.innerHTML += `<option value="${acc.id}">${acc.type}</option>`;
                });
            }
        } catch(e) { console.warn(e); }
    }
    refreshBalance(); loadTransactions(); loadAIPrediction(); loadAIAdvice(); loadAccounts();
    setInterval(() => { loadAIPrediction(); refreshBalance(); }, 30000);
    
    document.getElementById('transfer-btn')?.addEventListener('click', async function() {
        const from_acc = document.getElementById('from-acc').value;
        const to_acc = document.getElementById('to-acc').value;
        const amount = parseFloat(document.getElementById('amount').value);
        if(!from_acc || !to_acc || isNaN(amount)) { alert('يرجى تعبئة جميع الحقول'); return; }
        const btn = this; btn.disabled = true; btn.innerHTML = '<i class="fa-regular fa-spinner fa-spin"></i> تحليل المخاطر ...';
        try {
            const res = await fetch('/api/transfer', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({from_account:from_acc, to_account:to_acc, amount}) });
            const result = await res.json();
            if(result.error) throw new Error(result.error);
            document.getElementById('risk-output').innerHTML = `✅ تم التحويل بنجاح. الرقم: ${result.transaction_id} | المخاطرة: ${result.risk.risk_score}`;
            await refreshBalance();
            await loadTransactions();
        } catch(err) { document.getElementById('risk-output').innerHTML = `❌ فشل: ${err.message}`; }
        finally { btn.disabled = false; btn.innerHTML = '<i class="fa-regular fa-shield"></i> تقييم وتنفيذ التحويل'; }
    });
</script>
</body>
</html>
'''

# -------------------- صفحات الويب الخلفية --------------------
@app.route('/')
@login_required
def dashboard():
    return render_template_string(HTML_MAIN)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and username in users_db and check_password_hash(users_db[username]['password_hash'], password):
            session['authenticated'] = True
            session['username'] = username
            session.permanent = True
            app.logger.info(f"تسجيل دخول ناجح للمستخدم {username}")
            flash(f"مرحباً {users_db[username]['full_name']}، تم الدخول إلى النظام المصرفي الذكي V87 على المنفذ 7000", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("بيانات الدخول غير صحيحة", "danger")
    return render_template_string('''
<!DOCTYPE html>
<html dir="rtl">
<head><meta charset="UTF-8"><title>تسجيل الدخول - Cherrak AI Bank | Port 7000</title><link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet"></head>
<body class="bg-black text-white flex items-center justify-center h-screen">
    <div class="bg-gray-900/70 p-10 rounded-3xl backdrop-blur border border-cyan-500 w-96">
        <h1 class="text-3xl font-black text-center text-cyan-400 mb-5">تسجيل الدخول الآمن</h1>
        <div class="text-center text-xs text-gray-500 mb-3">المنفذ: 7000 | Cherrak Bank V87</div>
        {% with messages = get_flashed_messages(with_categories=true) %}{% for cat,msg in messages %}<div class="bg-red-800 p-2 rounded mb-3">{{ msg }}</div>{% endfor %}{% endwith %}
        <form method="POST">
            <input type="text" name="username" placeholder="اسم المستخدم" class="w-full p-3 rounded-xl bg-gray-800 mb-3 border border-gray-700">
            <input type="password" name="password" placeholder="كلمة المرور" class="w-full p-3 rounded-xl bg-gray-800 mb-5">
            <button class="w-full bg-cyan-600 p-3 rounded-xl font-bold">دخول إلى المنصة الذكية</button>
        </form>
        <div class="text-xs text-gray-500 mt-5 text-center">نسخة V87 | تشفير عسكري | AI Risk Engine | Port 7000</div>
    </div>
</body>
</html>
''')

@app.route('/logout')
def logout():
    session.clear()
    flash("تم تسجيل الخروج بنجاح", "info")
    return redirect(url_for('login_page'))

# ============================== تشغيل الخادم على المنفذ 7000 ==============================
if __name__ == '__main__':
    # تحديد المنفذ 7000 بشكل قاطع
    PORT = 7000
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║     ██████╗██╗  ██╗███████╗██████╗ ██████╗  █████╗ ██╗  ██╗  ║
    ║     ██╔════╝██║  ██║██╔════╝██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝  ║
    ║     ██║     ███████║█████╗  ██████╔╝██████╔╝███████║█████╔╝   ║
    ║     ██║     ██╔══██║██╔══╝  ██╔══██╗██╔══██╗██╔══██║██╔═██╗   ║
    ║     ╚██████╗██║  ██║███████╗██║  ██║██║  ██║██║  ██║██║  ██╗  ║
    ║     ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝  ║
    ║                                                              ║
    ║        CHERRAK BANK AI - V87 SOVEREIGN ETHER CORE           ║
    ║                    التشغيل على المنفذ: 7000                  ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    app.logger.info(f'تشغيل Cherrak Bank AI V87 على المنفذ {PORT}')
    app.run(host='0.0.0.0', port=PORT, debug=False, threaded=True)
