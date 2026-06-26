import streamlit as st
import json
import os

# ============================================
# DecodeLabs - Project 2: Expense Tracker
# Accumulator Pattern: total += new_expense
# ============================================

DATA_FILE = "expenses.json"

def load_expenses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_expenses(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=4)

st.set_page_config(page_title="Expense Tracker", page_icon="💸", layout="wide")

# ---------- SESSION STATE ----------
if "expenses" not in st.session_state:
    st.session_state.expenses = load_expenses()
if "next_id" not in st.session_state:
    ids = [e["id"] for e in st.session_state.expenses]
    st.session_state.next_id = max(ids) + 1 if ids else 1

expenses = st.session_state.expenses

# ---------- SIDEBAR — ADD EXPENSE ----------
with st.sidebar:
    st.markdown("## 💸 Expense Tracker")
    st.markdown("*DecodeLabs • Project 2*")
    st.divider()

    st.markdown("### ➕ New Expense")

    desc = st.text_input("Description", placeholder="e.g. Coffee, Rent...")
    amount_str = st.text_input("Amount (Rs.)", placeholder="e.g. 500")
    category = st.radio(
        "Category",
        ["🍔 Food", "🚗 Transport", "🛍️ Shopping", "📄 Bills", "💊 Health", "📦 Other"],
        horizontal=False
    )

    if st.button("Add Expense", type="primary", use_container_width=True):
        if desc.strip() == "":
            st.error("Enter a description!")
        elif amount_str.strip() == "":
            st.error("Enter an amount!")
        else:
            try:
                amount = float(amount_str)
                if amount <= 0:
                    st.error("Amount must be positive!")
                else:
                    st.session_state.expenses.append({
                        "id": st.session_state.next_id,
                        "description": desc.strip(),
                        "category": category.split(" ", 1)[1],
                        "amount": amount
                    })
                    st.session_state.next_id += 1
                    save_expenses(st.session_state.expenses)
                    st.success("Added!")
                    st.rerun()
            except ValueError: 
                st.error("Invalid! Enter numbers only.")

    st.divider()
    if len(expenses) > 0:
        if st.button("🗑 Clear All", use_container_width=True):
            st.session_state.expenses = []
            save_expenses([])
            st.rerun()

# ---------- MAIN PAGE ----------
st.markdown("# 📊 Financial Dashboard")
st.markdown("Track every rupee. Know where it goes.")
st.divider()

# ---------- STATS ROW ----------
total = sum(e["amount"] for e in expenses) 
count = len(expenses)
avg = total / count if count > 0 else 0
biggest = max((e["amount"] for e in expenses), default=0)

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Spent", f"Rs. {total:,.0f}")
col2.metric("🧾 Transactions", count)
col3.metric("📊 Average", f"Rs. {avg:,.0f}")
col4.metric("📈 Biggest", f"Rs. {biggest:,.0f}")

st.divider()

if len(expenses) == 0:
    st.markdown("### No expenses yet!")
    st.info("👈 Add your first expense from the sidebar.")
else:
    left, right = st.columns([0.6, 0.4])

    # ---------- LEFT — EXPENSE TABLE ----------
    with left:
        st.markdown("### 🧾 All Transactions")

        for e in reversed(expenses):   # newest first
            c1, c2, c3 = st.columns([0.55, 0.25, 0.2])
            with c1:
                st.markdown(f"**{e['description']}**  \n`{e['category']}`")
            with c2:
                st.markdown(f"### Rs. {e['amount']:,.0f}")
            with c3:
                if st.button("✕", key=f"del_{e['id']}"):
                    st.session_state.expenses = [
                        x for x in st.session_state.expenses if x["id"] != e["id"]
                    ]
                    save_expenses(st.session_state.expenses)
                    st.rerun()
            st.markdown("---")

    # ---------- RIGHT — CATEGORY BREAKDOWN ----------
    with right:
        st.markdown("### 📂 By Category")

        category_totals = {}
        for e in expenses:
            cat = e["category"]
            category_totals[cat] = category_totals.get(cat, 0) + e["amount"]

        for cat, cat_total in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
            pct = (cat_total / total * 100) if total > 0 else 0
            st.markdown(f"**{cat}** — Rs. {cat_total:,.0f} &nbsp;&nbsp; `{pct:.1f}%`")
            st.progress(pct / 100)
            st.markdown("")

        st.divider()
        st.markdown("### 📋 Summary")
        st.markdown(f"- **Highest Category:** {max(category_totals, key=category_totals.get)}")
        st.markdown(f"- **Total Categories:** {len(category_totals)}")
        st.markdown(f"- **Total Transactions:** {count}")
        st.markdown(f"- **Grand Total:** Rs. {total:,.2f}")

if __name__ == "__main__":
    pass
