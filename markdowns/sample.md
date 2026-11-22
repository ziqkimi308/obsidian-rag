# Quokka Coffee Co. Operations Wiki

Version 2.1 | Last updated 12 January 2026

## 1. Company Overview

Quokka Coffee Co. is a fictional specialty coffee chain founded in 2021 by Mei Tan. It runs 4 outlets: Bangsar, Ipoh, Subang Jaya, and Melaka. The head office is in Petaling Jaya. The chain employs 46 staff in total.

## 2. Opening Hours

- Monday to Saturday: 7:30 AM to 9:00 PM
- Sunday: 9:00 AM to 6:00 PM
- Public holidays: same as Sunday hours, except Chinese New Year (closed for 2 days)

## 3. Opening Checklist

1. Switch on the espresso machine 30 minutes before opening.
2. Calibrate the grinder: target 18 g in, 36 g out, in 28 seconds.
3. Count the till float. The standard float is RM 200.
4. Wipe down all tables and restock napkins and straws.
5. Unlock the front door at the scheduled opening time, not earlier.

## 4. Menu and Prices

| Drink | Price (RM) | Notes |
|-------|-----------|-------|
| Latte | 12 | Hot or iced |
| Flat White | 13 | Hot only |
| Cold Brew | 14 | Steeped for 18 hours |
| Matcha Latte | 15 | Uses ceremonial grade matcha |
| Americano | 9 | Hot or iced |

Oat milk costs an extra RM 2 per drink. A decaf shot is an extra RM 1.

## 5. Loyalty Program

Each drink earns 1 stamp. Collecting 8 stamps gives one free drink of any size. Stamps expire 90 days after they are earned. Customers who buy 50 drinks within one calendar year become Gold members and get 10% off every purchase.

## 6. Equipment Maintenance

### 6.1 Daily

- Backflush the espresso machine at closing.
- Empty and rinse the knock box.

### 6.2 Periodic

- Descale the espresso machine every 3 months.
- Replace grinder burrs every 6 months or after 800 kg of beans, whichever comes first.
- Replace water filters every 4 months.

If any machine breaks down during opening hours, call the technician Raj Kumar on extension 204.

## 7. Suppliers and Deliveries

Coffee beans come from Kopi Hijau Roasters in Cameron Highlands and are delivered every Wednesday. Fresh milk comes from Dairy Hill and is delivered on Mondays and Thursdays. Pastries are baked in-house at the Bangsar outlet and sent to other outlets each morning by 6:30 AM.

## 8. POS Configuration

The point-of-sale system uses the following settings:

```yaml
pos:
  tax_rate: 6%
  currency: MYR
  receipt_footer: "Thank you for visiting Quokka Coffee!"
  auto_logout_minutes: 10
  refund_limit_without_manager: 30
```

## 9. Customer Complaints

Staff may issue a refund or replacement of up to RM 30 without manager approval. Anything above RM 30 needs approval from the outlet manager. All complaints must be logged in the shared incident sheet before the end of the shift. The Head of Operations is Hafiz Rahim.