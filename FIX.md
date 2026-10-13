# 🚨 URGENT: CRITICAL SYSTEM REFACTOR & USER REQUIREMENTS  
**Priority:** P0 (Blocks all user workflows)  
**Deadline:** Fix truncated files + POS/reports within 48 hours  

## 🎯 CORE USER REQUIREMENTS (NON-NEGOTIABLE)  
1. **POS PAGE REDESIGN**  
   - ❌ REMOVE: All confusing workflows, supplier procurement logic, complex menus  
   - ✅ BUILD: *Dead-simple sales interface only*:  
     • Search parts by SKU/name → Add to cart → Process payment → Print receipt  
     • **Critical**: Parts used in service orders MUST pull from *same inventory* as POS sales  
     • *Procurement (buying from suppliers) is a SEPARATE workflow* – do NOT clutter POS page  
   - 🔒 FIX: Atomic stock deduction (prevent overselling via `SELECT FOR UPDATE`)  

2. **REPORTS MUST WORK**  
   - Revenue Report: Daily/weekly/monthly graphs (bar/line charts), export to CSV/PDF  
   - Order Inventory Report: Parts used per service order, stock levels, low-stock alerts  
   - ✅ REQUIREMENTS:  
     • Zero blank screens – show "No data" with date filters if empty  
     • Load in <3s (fix N+1 queries with `joinedload()`)  
     • Export buttons functional with timestamped filenames  
     • Visualize trends (e.g., "Top 10 Sold Parts" pie chart)  

## 🔧 CRITICAL TECHNICAL FIXES (FROM CODE REVIEW)  
| Area | Action | Why It Matters |  
|------|--------|----------------|  
| **Session Management** | NEVER store DB sessions in `st.session_state`. Use context managers + `finally` blocks to close sessions | Prevents memory leaks/crashes |  
| **Truncated Files** | Fix `config.py` (complete CURRENCY_SYMBOL string) + `validators.py` (complete regex) | App won't launch otherwise |  
| **Inventory Safety** | Rewrite stock deduction in `pos_service.py` + `service_order_service.py` with DB-level locking | Stops negative stock/data corruption |  
| **Decimal Precision** | Audit ALL money calculations: Replace `float` → `Decimal` everywhere (models, services, UI) | Prevents financial rounding errors |  
| **Reports Data** | Add eager loading (`joinedload`), date-range filters, error boundaries | Fixes blank reports + slow loads |  
| **Security** | Remove password dicts from session_state; add login rate limiting | Blocks brute-force attacks |  

## 🚫 ABSOLUTELY AVOID  
- Adding procurement/supplier workflows to POS page (user requirement: *"POS makes no sense"*)  
- File-based storage (e.g., `pos_frequency.json`) → Migrate to DB  
- Hardcoded limits (e.g., `get_recent(5)`) → Make configurable  
- `st.rerun()` spam → Use Streamlit state callbacks  

## ✅ SUCCESS METRICS  
- [ ] POS page loads in <2s, processes sale in <15 seconds  
- [ ] Revenue Report shows accurate graphs + exports working CSV  
- [ ] Zero console errors when adding parts to service orders  
- [ ] `pytest` passes on inventory deduction tests (simulate 10 concurrent sales)  
- [ ] App starts cleanly with `.env.example` documenting all required vars  

## 📌 FIRST STEPS (START NOW)  
1. Fix `config.py` and `validators.py` → Verify app launches  
2. Redesign POS page UI *before* touching backend (share mockup for approval)  
3. Build report data pipelines with error logging (log failures to file)  
4. Write test for inventory race condition: "Can 5 users buy last item simultaneously?"  

> 💡 **Key Insight from Report**: *"This isn’t polish work – it’s rebuilding foundations. Do NOT skip tests on inventory logic. One race condition = lost customer trust."*  
> **Reference**: Full code review details critical flaws in session management (Section 1), inventory races (Section 5), and report failures (Section 25).  
