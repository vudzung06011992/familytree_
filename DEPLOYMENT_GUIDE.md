# Family Tree Web Application

## Deployment Instructions

### Option 1: Deploy với Vercel (Frontend) + Railway (Backend) - MIỄN PHÍ

#### A. Deploy Backend (Python Flask) lên Railway:

1. **Đăng ký tài khoản Railway:**
   - Truy cập: https://railway.app
   - Đăng ký bằng GitHub account

2. **Tạo project mới:**
   - Click "New Project" 
   - Chọn "Deploy from GitHub repo"
   - Connect GitHub repository này

3. **Cấu hình Railway:**
   - Railway sẽ tự động detect Python app
   - Kiểm tra `requirements.txt` và `Procfile` đã có
   - Deploy sẽ tự động chạy

4. **Lấy URL backend:**
   - Sau khi deploy thành công, copy URL (dạng: https://xxx.railway.app)

#### B. Cập nhật Frontend với URL backend:

1. **Mở file `index.html`**
2. **Tìm dòng:** `return 'https://YOUR_RAILWAY_URL.railway.app';`
3. **Thay thế** `YOUR_RAILWAY_URL` bằng URL Railway thực tế

#### C. Deploy Frontend lên Vercel:

1. **Đăng ký Vercel:**
   - Truy cập: https://vercel.com
   - Đăng ký bằng GitHub account

2. **Import project:**
   - Click "New Project"
   - Import repository này từ GitHub
   - Vercel sẽ tự động deploy với `vercel.json` config

3. **Truy cập website:**
   - Vercel sẽ cung cấp URL (dạng: https://xxx.vercel.app)

### Option 2: Deploy với Netlify (Frontend) + Heroku (Backend)

#### A. Deploy Backend lên Heroku:

1. **Cài đặt Heroku CLI:** https://devcenter.heroku.com/articles/heroku-cli

2. **Commands:**
   ```bash
   heroku login
   heroku create your-familytree-api
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

#### B. Deploy Frontend lên Netlify:

1. **Drag & Drop method:**
   - Truy cập: https://netlify.com
   - Kéo thả folder project vào Netlify
   - Cập nhật URL backend trong `index.html`

### Option 3: GitHub Pages (Chỉ Frontend - Static only)

**Lưu ý:** GitHub Pages chỉ host static files, không chạy được Python backend.

1. **Cấu hình GitHub Pages:**
   - Settings > Pages > Source: Deploy from branch `main`

2. **Sử dụng backend khác:**
   - Cần deploy Python server riêng (Railway/Heroku)
   - Hoặc convert sang static solution

## Cấu hình Production

### Backend (server.py):
- ✅ CORS đã cấu hình cho multiple domains
- ✅ PORT từ environment variable
- ✅ Host 0.0.0.0 cho production

### Frontend (index.html):
- ✅ Auto-detect local vs production environment
- ✅ Dynamic API URL configuration

## Files được tạo cho deployment:
- `requirements.txt` - Python dependencies
- `Procfile` - Railway/Heroku config  
- `vercel.json` - Vercel config

## Troubleshooting:

### CORS errors:
- Đảm bảo frontend URL được thêm vào CORS config trong `server.py`

### Backend không chạy:
- Kiểm tra logs trên Railway/Heroku dashboard
- Đảm bảo `requirements.txt` có đầy đủ dependencies

### File upload không hoạt động:
- Kiểm tra API URL trong browser developer tools
- Đảm bảo backend endpoint `/upload` hoạt động

## Live URLs (sau khi deploy):
- Frontend: https://your-project.vercel.app
- Backend API: https://your-project.railway.app
