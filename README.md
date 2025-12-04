# ShareHub (Social Media Website)

### Live Demo  
https://social-media-sharehub.netlify.app/

### Frontend Repository  
https://github.com/ShaadSD/Social-Media-ShareHub-Frontend-

---

A fully featured **backend-only social media platform**, built using **Django** and **REST principles**.  
This API powers user authentication, following system, posts, likes, comments, and contact messages ready to be used by any frontend.

This project focuses on **clean architecture**, **secure authentication**, **scalable models**, and **well-structured API endpoints**.

---

# Features Overview

## User Authentication
- Register, login, logout  
- Email verification (activation link)  
- Password reset & password change  
- Token-based authentication  

## Social Features
- Follow / unfollow users  
- Followers management  
- Profile view & update  
- People You May Know recommendation  

## Post System
- Create, read, update, delete posts  
- Image/video upload supported  
- Like / Unlike posts  
- Comment system (full CRUD support)  

## Contact System
- Send contact messages  
- Store inquiries for admin panel  

## Security
- Protected endpoints require authentication  
- Clean JSON responses  
- Secure handling of user data  

---

# Tech Stack

| Component | Tools |
|----------|--------|
| Backend Framework | Django |
| API Layer | Django REST Framework |
| Authentication | Token-based Auth |
| Database |PostgreSQL |

---

# API Endpoints Documentation

All endpoints are prefixed with:

---

## Authentication & Account Management

| Action | Method | Endpoint |
|--------|--------|-----------|
| Register | POST | `/api/user/register/` |
| Login | POST | `/api/user/login/` |
| Logout | POST | `/api/user/logout/` |
| Activate Account | GET | `/api/user/active/<uid64>/<token>/` |
| Password Change | POST | `/api/password/change/` |
| Password Reset Request | POST | `/api/password/reset/` |
| Password Reset Confirm | POST | `/api/password/reset/confirm/` |

---

## Profile & Social Features

| Action | Method | Endpoint |
|--------|--------|-----------|
| Get / Update Profile | GET / PUT | `/api/profile/` |
| Follow / Unfollow User | POST | `/api/follow/` |
| Followers List | GET | `/api/followers/` |
| Manage Followers | POST | `/api/followers/manage/` |
| People You May Know | GET | `/api/people-you-may-know/` |

---

## Posts API

| Action | Method | Endpoint |
|--------|--------|-----------|
| List / Create Posts | GET / POST | `/api/posts/` |
| Post Detail | GET / PUT / DELETE | `/api/posts/<post_id>/` |

---

## Likes

| Action | Method | Endpoint |
|--------|--------|-----------|
| Like / Unlike Post | POST | `/api/posts/<post_id>/like/` |

---

## Comments

| Action | Method | Endpoint |
|--------|--------|-----------|
| Create / Get Comments | POST / GET | `/api/posts/comments/` |
| Comment Detail | GET / PUT / DELETE | `/api/posts/comments/<comments_id>/` |

---

## Contact Message

| Action | Method | Endpoint |
|--------|--------|-----------|
| Send Contact Form | POST | `/api/contact/` |

---



