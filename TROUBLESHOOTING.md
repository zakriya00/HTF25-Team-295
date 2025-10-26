# 🔧 Troubleshooting Guide
## StudySync - Real-Time Study Room Chat Application

---

## 🚨 **White Page Issue - Step by Step Fix**

### **Step 1: Check Backend Server**
```bash
# Make sure you're in the project root directory
cd HTF25-Team-295

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies (if not done)
pip install -r requirements.txt

# Initialize database with new gamification tables
python -m app.init_db

# Start backend server
python -m uvicorn app.main:app --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### **Step 2: Check Frontend Server**
```bash
# In a new terminal, navigate to frontend
cd studyroom-frontend

# Install dependencies (if not done)
npm install

# Start frontend server
npm run dev
```

**Expected Output:**
```
  VITE v7.1.7  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

### **Step 3: Test Backend API**
```bash
# Test if backend is responding
python test_backend.py
```

**Expected Output:**
```
✅ Basic endpoint: 200
Response: {'message': 'Real-Time Study Room Chat API running!'}
✅ Gamification endpoint: 200
✅ Chat endpoint: 200
```

---

## 🔍 **Common Issues & Solutions**

### **Issue 1: Backend Not Starting**
**Symptoms:** Backend server fails to start or crashes

**Solutions:**
1. **Check Python version:**
   ```bash
   python --version
   # Should be Python 3.12+
   ```

2. **Check dependencies:**
   ```bash
   pip list | grep fastapi
   pip list | grep uvicorn
   ```

3. **Reinstall dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Check for port conflicts:**
   ```bash
   netstat -an | findstr :8000
   # If port 8000 is in use, kill the process or use different port
   ```

### **Issue 2: Database Errors**
**Symptoms:** Database-related errors in backend logs

**Solutions:**
1. **Delete old database and recreate:**
   ```bash
   # Delete the old database file
   rm studychat.db
   # or on Windows:
   del studychat.db
   
   # Recreate database
   python -m app.init_db
   ```

2. **Check database file permissions:**
   ```bash
   ls -la studychat.db
   # Make sure the file is writable
   ```

### **Issue 3: Frontend White Page**
**Symptoms:** Frontend loads but shows white page

**Solutions:**
1. **Check browser console:**
   - Open browser developer tools (F12)
   - Look for JavaScript errors in Console tab
   - Check Network tab for failed requests

2. **Check if backend is running:**
   - Open http://localhost:8000 in browser
   - Should show: `{"message":"Real-Time Study Room Chat API running!"}`

3. **Clear browser cache:**
   - Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
   - Or clear browser cache completely

4. **Check CORS issues:**
   - Look for CORS errors in browser console
   - Backend should have CORS enabled for localhost:5173

### **Issue 4: Gamification Features Not Working**
**Symptoms:** App loads but gamification features don't work

**Solutions:**
1. **Check if gamification tables exist:**
   ```bash
   python -c "from app.database import engine; from sqlalchemy import inspect; print(inspect(engine).get_table_names())"
   ```
   Should show: `['users', 'rooms', 'messages', 'muted_users', 'user_profiles', 'badges', 'user_badges', 'daily_challenges', 'challenge_submissions']`

2. **Test gamification API directly:**
   ```bash
   curl http://localhost:8000/gamification/user-stats/testuser
   ```

3. **Check browser console for API errors:**
   - Look for 404 or 500 errors in Network tab
   - Check if gamification endpoints are accessible

---

## 🛠 **Debugging Steps**

### **Step 1: Verify Backend Health**
```bash
# Test basic endpoint
curl http://localhost:8000/

# Test gamification endpoint
curl http://localhost:8000/gamification/user-stats/testuser

# Test chat endpoint
curl http://localhost:8000/chat/history/testroom
```

### **Step 2: Check Frontend Console**
1. Open browser developer tools (F12)
2. Go to Console tab
3. Look for any red error messages
4. Check Network tab for failed requests

### **Step 3: Verify Database**
```bash
# Check if database file exists
ls -la studychat.db

# Check database tables
python -c "from app.database import engine; from sqlalchemy import inspect; print(inspect(engine).get_table_names())"
```

### **Step 4: Test Step by Step**
1. **Test basic chat first:**
   - Join a room
   - Send a message
   - Check if message appears

2. **Test gamification:**
   - Click trophy button in header
   - Check if sidebar opens
   - Look for any errors in console

---

## 🚀 **Quick Fix Commands**

### **Complete Reset (if nothing works):**
```bash
# 1. Stop all servers (Ctrl+C)

# 2. Clean up
rm studychat.db
rm -rf studyroom-frontend/node_modules
rm studyroom-frontend/package-lock.json

# 3. Reinstall everything
pip install -r requirements.txt
cd studyroom-frontend
npm install

# 4. Recreate database
cd ..
python -m app.init_db

# 5. Start servers
python -m uvicorn app.main:app --reload
# In new terminal:
cd studyroom-frontend
npm run dev
```

### **Minimal Test (without gamification):**
If gamification is causing issues, you can temporarily disable it:

1. **Comment out gamification imports in ChatRoom.jsx:**
   ```javascript
   // import GamificationSidebar from "./GamificationSidebar";
   // import GamificationNotification from "./GamificationNotification";
   // import { GamificationProvider, useGamification } from "../context/GamificationContext";
   ```

2. **Comment out gamification usage:**
   ```javascript
   // const { userStats, fetchUserStats } = useGamification();
   ```

3. **Remove gamification components from render:**
   ```javascript
   // <GamificationSidebar ... />
   // <GamificationNotification ... />
   ```

---

## 📞 **Getting Help**

### **Check Logs:**
1. **Backend logs:** Look at terminal where uvicorn is running
2. **Frontend logs:** Check browser console (F12)
3. **Database logs:** Check if database file is being created

### **Common Error Messages:**
- **"Module not found"** → Run `npm install` or `pip install -r requirements.txt`
- **"Port already in use"** → Kill process using port 8000 or 5173
- **"Database locked"** → Delete studychat.db and recreate
- **"CORS error"** → Check backend CORS settings
- **"White page"** → Check browser console for JavaScript errors

### **Test Checklist:**
- [ ] Backend server running on http://localhost:8000
- [ ] Frontend server running on http://localhost:5173
- [ ] Database file exists (studychat.db)
- [ ] No errors in backend terminal
- [ ] No errors in browser console
- [ ] Can access http://localhost:8000 in browser
- [ ] Can access http://localhost:5173 in browser

---

## 🎯 **Expected Behavior**

### **Working App Should:**
1. **Load landing page** with username/room input
2. **Allow joining room** after entering username and room name
3. **Show chat interface** with message input and send button
4. **Display trophy button** in header (gamification)
5. **Allow sending messages** that appear in real-time
6. **Show user stats** in header (points, level, streak)
7. **Open gamification sidebar** when trophy button is clicked

### **If Something Doesn't Work:**
1. Check browser console for errors
2. Check backend terminal for errors
3. Verify all servers are running
4. Test API endpoints directly
5. Check database tables exist

---

This troubleshooting guide should help you resolve the white page issue and get your gamified study chat application running properly! 🚀
