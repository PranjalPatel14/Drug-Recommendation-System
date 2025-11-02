# Deployment Guide for Drug Recommendation System

This guide covers multiple deployment options for your Flask-based Drug Recommendation System.

## 📋 Prerequisites

1. **Python 3.8+** installed on your system
2. **Trained model** (`dataset/model.joblib`) - Make sure you've run `train_model.py` first
3. **All dataset files** in the `dataset/` folder
4. **Git** (for version control and deployment)

---

## 🚀 Deployment Options

### Option 1: Deploy to Render (Recommended for Beginners)

[Render](https://render.com) offers a free tier and easy deployment.

#### Steps:
1. **Create a Render account** at https://render.com
2. **Create a new Web Service**:
   - Connect your GitHub repository
   - Or upload your project directly
3. **Configure the service**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn wsgi:app --bind 0.0.0.0:$PORT`
   - **Environment**: Python 3
4. **Add Environment Variables** (if needed):
   - No special environment variables required for basic deployment
5. **Deploy!**

Your app will be available at: `https://your-app-name.onrender.com`

---

### Option 2: Deploy to Railway

[Railway](https://railway.app) is another excellent free option.

#### Steps:
1. **Sign up** at https://railway.app
2. **Create a new project** and connect your GitHub repo
3. **Add a new Web Service**:
   - Railway will auto-detect it's a Python app
   - It will use the `Procfile` automatically
4. **Configure**:
   - Set Python version to 3.8+
   - Railway will install dependencies from `requirements.txt`
5. **Deploy!**

---

### Option 3: Deploy to Heroku

[Heroku](https://heroku.com) (Note: Free tier discontinued, but still a good option)

#### Steps:
1. **Install Heroku CLI**: https://devcenter.heroku.com/articles/heroku-cli
2. **Login**:
   ```bash
   heroku login
   ```
3. **Create a Heroku app**:
   ```bash
   heroku create your-app-name
   ```
4. **Deploy**:
   ```bash
   git add .
   git commit -m "Deploy app"
   git push heroku main
   ```
5. **Open your app**:
   ```bash
   heroku open
   ```

---

### Option 4: Deploy to PythonAnywhere

[PythonAnywhere](https://www.pythonanywhere.com) offers free hosting.

#### Steps:
1. **Sign up** at https://www.pythonanywhere.com
2. **Upload your files**:
   - Use the Files tab to upload your project
   - Or clone from GitHub if you have a repository
3. **Set up a Web App**:
   - Go to Web tab → Create a new web app
   - Choose Flask and Python 3.8+
   - Set the source code directory to your project folder
4. **Configure WSGI file**:
   - Edit the WSGI file to point to `wsgi.py`
   - Example:
     ```python
     import sys
     path = '/home/yourusername/path/to/your/app'
     if path not in sys.path:
         sys.path.append(path)
     
     from wsgi import app
     application = app
     ```
5. **Reload the web app**

---

### Option 5: Deploy to AWS (EC2/Elastic Beanstalk)

#### Using AWS Elastic Beanstalk (Easier):

1. **Install EB CLI**:
   ```bash
   pip install awsebcli
   ```
2. **Initialize EB**:
   ```bash
   eb init
   ```
3. **Create and deploy**:
   ```bash
   eb create drug-recommendation-env
   eb deploy
   ```

#### Using EC2 (More control):

1. **Launch an EC2 instance** (Ubuntu recommended)
2. **SSH into the instance**
3. **Install dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3-pip nginx
   pip3 install -r requirements.txt
   ```
4. **Run with Gunicorn**:
   ```bash
   gunicorn --bind 0.0.0.0:8000 wsgi:app
   ```
5. **Configure Nginx** as a reverse proxy

---

### Option 6: Deploy Locally with Gunicorn

For testing production-like setup locally:

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run with Gunicorn**:
   ```bash
   gunicorn wsgi:app --bind 0.0.0.0:8000 --workers 2
   ```

3. **Access at**: http://localhost:8000

---

## 🔧 Production Configuration

### Update app.py for Production

Modify the last line in `app.py`:

```python
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
```

This ensures:
- Debug mode is OFF (important for security)
- App listens on all interfaces
- Port is configurable via environment variable

### Environment Variables

Some platforms allow you to set environment variables:
- `PORT`: Server port (usually set automatically by hosting platform)
- `FLASK_ENV`: Set to `production` for production mode

---

## ✅ Pre-Deployment Checklist

- [ ] Run `train_model.py` to ensure `dataset/model.joblib` exists
- [ ] Verify all CSV files are in the `dataset/` folder
- [ ] Test the app locally (`python app.py`)
- [ ] Ensure `requirements.txt` includes all dependencies
- [ ] Check that `dataset/` folder will be included in deployment (not in `.gitignore`)
- [ ] Update `app.py` to disable debug mode for production

---

## 🐛 Troubleshooting

### Common Issues:

1. **Model not found**:
   - Ensure `train_model.py` has been run
   - Check that `dataset/model.joblib` exists in the deployment

2. **Dataset files not found**:
   - Verify all CSV files are uploaded to the hosting platform
   - Check file paths are relative (not absolute)

3. **Port errors**:
   - Use `$PORT` environment variable or `0.0.0.0` binding
   - Check platform-specific port requirements

4. **Memory issues**:
   - Some free tiers have memory limits
   - Consider optimizing model size or upgrading plan

---

## 📝 Additional Notes

- **Free tier limitations**: Most free hosting services have limits on:
  - Request timeouts (usually 30-60 seconds)
  - Memory usage
  - Request frequency
  - Uptime (some spin down after inactivity)

- **For production use**, consider:
  - Paid hosting plans for better performance
  - Database integration for logging predictions
  - API rate limiting
  - HTTPS/SSL certificates (usually provided by hosting platforms)
  - Monitoring and logging services

---

## 🔒 Security Considerations

1. **Disable debug mode** in production
2. **Don't commit sensitive data** (use environment variables)
3. **Add input validation** for symptoms
4. **Implement rate limiting** to prevent abuse
5. **Use HTTPS** (most platforms provide this automatically)

---

## 📞 Need Help?

If you encounter issues:
1. Check the hosting platform's documentation
2. Review error logs in the platform's dashboard
3. Test locally first to isolate issues
4. Ensure all dependencies are correctly specified

Good luck with your deployment! 🚀

