import frappe
import random
import string


@frappe.whitelist(allow_guest=True)
def signup(full_name, email, phone, password, role):
    try:
        if not email and not phone:
            return {"status": "error", "error": "Please provide either an email address or phone number."}

        if email and frappe.db.exists("User", email):
            return {"status": "error", "error": "An account with this email already exists."}

        allowed_roles = ["Picker", "Collector", "Recycler", "Producer", "Upcycler", "Fleet Manager"]
        if role not in allowed_roles:
            return {"status": "error", "error": "Invalid role selected."}

        names = full_name.strip().split()
        first = names[0]
        last = " ".join(names[1:]) if len(names) > 1 else ""

        user_email = email if email else f"{phone.replace('+', '')}@matxchange.local"

        user = frappe.get_doc({
            "doctype": "User",
            "email": user_email,
            "first_name": first,
            "last_name": last,
            "phone": phone,
            "mobile_no": phone,
            "enabled": 1,
            "new_password": password,
            "roles": [{"role": role}],
            "send_welcome_email": 0,
        })
        user.insert(ignore_permissions=True)
        frappe.db.commit()

        if email:
            try:
                frappe.sendmail(
                    recipients=[email],
                    sender="hello@matxchange.co.ke",
                    subject="Welcome to MatXchange",
                    message=f"""<div style="font-family:Inter,sans-serif;max-width:520px;margin:0 auto;background:#fff;border-radius:12px;overflow:hidden;border:1px solid #E5E7EB"><div style="background:#1A1A1A;padding:1.5rem;text-align:center"><img src="https://matxchange.co.ke/files/logo.png" height="40" alt="MatXchange" style="display:block;margin:0 auto"></div><div style="padding:2rem"><h2 style="color:#111;font-size:1rem;font-weight:600;margin-top:0">Welcome, {first}.</h2><p style="color:#374151;line-height:1.6;font-size:0.9rem">Your account has been created. You are registered as a <strong>{role}</strong>.</p><a href="https://matxchange.co.ke/login" style="display:inline-block;background:#1A1A1A;color:#fff;padding:0.7rem 1.25rem;border-radius:6px;text-decoration:none;font-size:0.85rem;margin-top:0.5rem">Log in</a><hr style="border:none;border-top:1px solid #F3F4F6;margin:1.5rem 0"><p style="color:#9CA3AF;font-size:0.75rem;margin:0">Matxchange Ltd · matxchange.co.ke</p></div></div>""",
                    now=True
                )
            except Exception:
                frappe.log_error(frappe.get_traceback(), "Welcome Email Error")

        return {"status": "success"}

    except frappe.exceptions.ValidationError as e:
        return {"status": "error", "error": str(e)}
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Signup Error")
        return {"status": "error", "error": "Signup failed. Please try again."}


@frappe.whitelist(allow_guest=True)
def send_otp(phone):
    try:
        otp = "".join(random.choices(string.digits, k=6))
        frappe.cache().set_value(f"otp_{phone}", otp, expires_in_sec=300)
        try:
            import africastalking
            api_key = frappe.conf.get("africas_talking_api_key")
            username = frappe.conf.get("africas_talking_username", "sandbox")
            africastalking.initialize(username, api_key)
            sms = africastalking.SMS
            sms.send(f"Your MatXchange code is: {otp}. Valid for 5 minutes.", [phone])
        except Exception:
            frappe.log_error(frappe.get_traceback(), "OTP SMS Error")
            return {"status": "error", "error": "Failed to send SMS."}
        return {"status": "success"}
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Send OTP Error")
        return {"status": "error", "error": "Failed to send OTP."}


@frappe.whitelist(allow_guest=True)
def verify_otp(phone, otp):
    try:
        stored = frappe.cache().get_value(f"otp_{phone}")
        if not stored:
            return {"status": "error", "error": "OTP expired. Request a new one."}
        if stored != otp:
            return {"status": "error", "error": "Invalid code. Try again."}
        user = frappe.db.get_value("User", {"mobile_no": phone}, "name")
        if not user:
            user = frappe.db.get_value("User", {"phone": phone}, "name")
        if not user:
            return {"status": "error", "error": "No account found. Please sign up first."}
        frappe.local.login_manager.login_as(user)
        frappe.cache().delete_value(f"otp_{phone}")
        return {"status": "success"}
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Verify OTP Error")
        return {"status": "error", "error": "Verification failed."}
