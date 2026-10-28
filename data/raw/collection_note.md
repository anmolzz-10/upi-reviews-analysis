# Data collection note

- Source: Google Play Store public reviews (country=in, language=en)
- Collected on: 2026-10-27
- Apps: PhonePe, Google Pay, Paytm, CRED, BHIM
- Method: google-play-scraper library, newest first, up to 80,000 reviews per app or last 60 days
- Total reviews: 66,475
- Privacy: reviewer names and profile pictures were not stored
- Limitation: a snapshot of public reviews; reviews skew toward extreme opinions and do not represent all users

```
            reviews          first_date           last_date  avg_rating  days_covered
app                                                                                  
BHIM           4257 2026-08-28 17:17:08 2026-10-26 17:10:05        2.77            58
CRED           1749 2026-08-28 18:59:08 2026-10-26 16:48:26        3.36            58
Google Pay     8559 2026-08-28 17:12:01 2026-10-26 17:15:01        4.08            59
Paytm         21951 2026-08-28 17:12:37 2026-10-26 17:15:31        4.48            59
PhonePe       29959 2026-08-28 17:14:04 2026-10-26 17:10:20        4.38            58
```
