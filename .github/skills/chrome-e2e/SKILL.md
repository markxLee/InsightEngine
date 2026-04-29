---
name: chrome-e2e
description: |
  E2E testing via Chrome DevTools MCP — test authenticated flows (Google OAuth, SSO, sessions)
  by connecting to the user's real Chrome browser with existing login state. Also provides
  DevTools-level debugging: performance traces, Lighthouse audits, network inspection, console
  monitoring, and memory profiling — capabilities Playwright cannot offer.
  Use this skill when: the user needs E2E tests through their real browser, testing requires
  auth/cookies/sessions, testing Google OAuth or SSO flows, debugging live pages with DevTools,
  running Lighthouse or performance analysis, or sites block bot-driven browsers.
  Triggers: "test qua Chrome", "kiểm tra e2e", "test trên trình duyệt thật", "test auth flow",
  "test Google login", "chạy e2e qua MCP", "test SSO flow", "E2E test with auth",
  "check my app in Chrome", "run lighthouse", "kiểm tra performance", "debug trên Chrome",
  "chạy Lighthouse", "test trang web", "check network requests", "test live site".
  Prefer over webapp-testing when auth/cookies matter or DevTools features are needed.
  Prefer webapp-testing when reusable Python test scripts or CI integration are needed.
---

# Chrome E2E — End-to-End Testing via Chrome DevTools MCP

Test web applications directly through Chrome using MCP tools — no Playwright scripts needed.
The key advantage: you can connect to the user's real Chrome browser, inheriting all login
sessions, cookies, and extensions. This makes testing authenticated flows (Google OAuth, SSO,
session-based auth) straightforward instead of painful.

## When to Use This vs webapp-testing

```
User request → Does it need auth/cookies from real browser?
  ├─ Yes → chrome-e2e (this skill)
  │    Examples: "test my app after Google login", "verify dashboard behind SSO"
  │
  └─ No → Does user want Chrome DevTools features?
      ├─ Yes → chrome-e2e (performance traces, Lighthouse, network inspection)
      │
      └─ No → Is a repeatable Playwright script needed?
          ├─ Yes → webapp-testing (generates reusable .py scripts)
          └─ No → chrome-e2e is simpler for one-off checks
```

**webapp-testing** is better when: you need a reusable test script, CI integration, or
headless automation that doesn't depend on user's browser state.

**chrome-e2e** is better when: auth matters, you need DevTools-level inspection (performance,
network, console, Lighthouse), or you want to test against the exact browser the user sees.

### Why a Separate Skill (Not Extending webapp-testing)

The approaches are fundamentally different:
- **webapp-testing** generates Python Playwright scripts → user runs them repeatedly
- **chrome-e2e** orchestrates MCP tool calls directly → no scripts to write or maintain

Playwright alternatives considered:
- `storageState.json` can persist cookies, but can't handle Google OAuth bot detection
- `--channel chrome` uses Chrome binary but still runs Playwright automation (detectable)
- Cypress `cy.session()` has similar bot-detection limits

Chrome MCP with `--autoConnect` solves these by using the user's actual browser with real
human-initiated sessions — no automation flags, no bot detection.

---

## Connection Modes

There are two ways to use Chrome MCP — choose based on whether auth is needed.

### Mode 1: Default (Managed Chrome) — No Auth Needed

The MCP server starts its own Chrome instance with a dedicated profile. Good for testing
public pages or apps where you can log in manually during the test.

Config (already set up in `.vscode/mcp.json`):
```json
{
  "command": "npx",
  "args": ["-y", "chrome-devtools-mcp@latest"]
}
```

The profile persists at `~/.cache/chrome-devtools-mcp/chrome-profile-stable`, so cookies
and login state survive between sessions. If you log in once, subsequent tests can reuse
that session.

### Mode 2: autoConnect (Real Chrome) — Full Auth Inheritance

Connects to the user's actual running Chrome browser. All existing login sessions, cookies,
and extensions are immediately available.

Config change needed in `.vscode/mcp.json`:
```json
{
  "command": "npx",
  "args": ["-y", "chrome-devtools-mcp@latest", "--autoConnect"]
}
```

**Setup required (one-time):**
1. User opens Chrome → navigates to `chrome://inspect/#remote-debugging`
2. Enables remote debugging → allows incoming connections via the dialog
3. Restart VS Code to reconnect MCP server

**Security note:** autoConnect exposes all browser data to the MCP client. The user should
avoid browsing sensitive sites (banking, passwords) during the testing session. Recommend
disconnecting when done.

---

## Health Check — Always Start Here

Before any test, verify the MCP connection is alive:

```
1. Call list_pages
   ├─ Returns pages → Connection OK, proceed
   └─ Error/empty → MCP server not running, restart VS Code
2. If using autoConnect: verify user's Chrome tabs appear in the list
   ├─ Yes → Real Chrome connected, auth sessions available
   └─ No → Fallback to default mode (managed Chrome)
```

This takes 1 second and prevents wasting time on a dead connection.

---

## E2E Testing Workflow

Follow this sequence for any E2E test:

### Step 1: Reconnaissance — Understand the Page

```
1. Navigate to the target URL
2. Take a snapshot (a11y tree — preferred) to understand page structure
3. Optionally take a screenshot for visual context
```

The snapshot returns a tree of elements with unique `uid` identifiers. These uids are how
you reference elements for clicking, filling, hovering, etc. Always use the latest snapshot
— uids change after page mutations.

### Step 2: Interact — Perform User Actions

Use MCP tools to simulate user behavior:

| Action | Tool | Key Parameter |
|--------|------|---------------|
| Click a button/link | `click` | `uid` of the element |
| Type into an input | `fill` | `uid` + `value` |
| Fill entire form | `fill_form` | array of `{uid, value}` |
| Hover over element | `hover` | `uid` |
| Press keyboard key | `press_key` | `key` (e.g., "Enter", "Tab") |
| Type freely | `type_text` | `text` + optional `submitKey` |
| Upload a file | `upload_file` | `uid` + `filePath` |
| Handle dialog/alert | `handle_dialog` | `action` ("accept"/"dismiss") |
| Drag and drop | `drag` | `from_uid` + `to_uid` |

After each interaction, take a new snapshot to see the updated state before continuing.

**Error recovery:** If a click or fill doesn't produce the expected result:
1. Take a fresh snapshot — the uid may have changed after a page mutation
2. Re-identify the target element in the new snapshot
3. Retry the interaction with the new uid
4. If still failing after 2 retries, take a screenshot and report the issue to the user

**Timeout guidance:** Use `wait_for` with explicit timeouts for navigation-heavy flows:
- Fast local pages: default timeout is fine
- OAuth redirects: `timeout: 30000` (30s) to allow for Google's redirect chain
- Slow APIs: `timeout: 15000` (15s) for data-heavy pages

### Step 3: Assert — Verify Expected State

There's no built-in assertion library — you verify by reading page state:

1. **Snapshot assertion**: Take snapshot, check that expected text/elements appear
2. **Screenshot assertion**: Take screenshot, visually verify layout
3. **Console check**: List console messages, verify no errors
4. **Network check**: List network requests, verify API calls succeeded
5. **Script evaluation**: Run JavaScript to extract specific values

Example assertion pattern:
```
Take snapshot → search for expected text in snapshot output →
  ├─ Found → assertion passes, continue
  └─ Not found → report failure with current page state
```

### Step 4: Report — Capture Evidence

For each test, capture:
- Screenshot of the final state
- Console messages (check for errors)
- Network requests (check for failed API calls)
- A summary of what was tested and the result

---

## Auth Flow Patterns

### Google OAuth Flow

This is the primary use case for `--autoConnect` mode. With the user's real Chrome:

1. Navigate to the app's login page
2. Take snapshot to find the "Sign in with Google" button
3. Click it → Google's OAuth page loads (user is already logged in to Google)
4. Google may auto-redirect back, or show account picker
5. If account picker: take snapshot → click the correct account
6. Wait for redirect back to the app
7. Take snapshot to verify logged-in state

If using default mode (not autoConnect), the OAuth flow requires manual user intervention
at the Google login step because the MCP Chrome won't have Google session cookies. In this
case:
1. Navigate to login page → click Google sign-in
2. Tell user: "Please complete the Google login in the MCP browser window"
3. Use `wait_for` tool with the expected post-login text
4. Continue testing once authenticated

### Session-Based Auth (Cookies)

With `--autoConnect`, existing session cookies are inherited automatically:
1. Navigate directly to the authenticated page
2. Take snapshot → verify you're logged in (not redirected to login)
3. If redirected → session expired, prompt user to log in manually first

With default mode, the MCP profile persists cookies between sessions:
1. First run: log in manually or programmatically
2. Subsequent runs: cookies persist → go directly to authenticated pages

### Token-Based Auth (Bearer/JWT)

For APIs or SPAs that use token auth:
1. Ask user for their token, or extract from environment variable
2. Use `evaluate_script` to inject into storage:
   ```
   Function: (token) => { localStorage.setItem('auth_token', token); }
   Args: ["<user-provided-token>"]
   ```
3. `navigate_page(type: "reload")` → the app reads the token and authenticates
4. `take_snapshot` → verify logged-in state appears

---

## Worked Example: Google OAuth E2E Test

A complete test flow showing every MCP tool call in sequence.

**Scenario:** Test that a user can sign in via Google OAuth on `localhost:3000`
and reach the dashboard.

```
# 0. Health check
list_pages → confirms connection OK

# 1. Navigate to app
navigate_page(url: "http://localhost:3000/login")
take_snapshot → find "Sign in with Google" button, note its uid (e.g. uid=1_5)

# 2. Click Google sign-in
click(uid: "1_5")
  → Page redirects to accounts.google.com

# 3. Handle Google account picker (autoConnect mode — already logged in)
take_snapshot → find the target Google account email, note uid
click(uid: "<account-uid>")
  → Google redirects back to localhost:3000/dashboard

# 4. Wait for redirect and verify
wait_for(text: ["Dashboard", "Welcome"])
take_snapshot → verify dashboard content loads correctly
  ├─ Expected: heading "Dashboard", user name displayed
  └─ If login page again: auth failed, check console for errors

# 5. Capture evidence
take_screenshot(filePath: "/tmp/e2e-google-auth-success.png")
list_console_messages(types: ["error"]) → verify no JS errors
list_network_requests → verify no failed API calls (4xx/5xx)

# 6. Test an authenticated action
take_snapshot → find a protected feature button
click(uid: "<feature-uid>")
wait_for(text: ["expected result"])
take_screenshot(filePath: "/tmp/e2e-auth-feature.png")
```

If NOT using autoConnect (Google login requires manual intervention):
- After step 2, tell user: "Please complete Google login in the MCP browser window"
- Use `wait_for(text: ["Dashboard"], timeout: 60000)` to wait up to 60s
- Continue from step 4 once redirected

---

## DevTools-Powered Testing

Capabilities beyond Playwright — use the matching MCP tool:

| Goal | Tool Sequence | Output |
|------|---------------|--------|
| **Performance** | `navigate_page` → `performance_start_trace(reload:true, autoStop:true)` | LCP, CLS, INP insights |
| **Deep perf insight** | (after trace) `performance_analyze_insight(insightName, insightSetId)` | Detailed breakdown |
| **Lighthouse** | `navigate_page` → `lighthouse_audit(mode:"navigation")` | A11y, SEO, best practices scores |
| **Network debug** | `navigate_page` → `list_network_requests` → `get_network_request(reqid)` | Headers, body, status |
| **Console errors** | `navigate_page` → `list_console_messages(types:["error"])` → `get_console_message(msgid)` | Error + stack trace |
| **Memory leak** | `navigate_page` → (reproduce issue) → `take_memory_snapshot(filePath)` | Heap snapshot file |

---

## Multi-Page Testing

Chrome MCP supports multiple tabs:

```
1. new_page → open a new tab with URL
2. list_pages → see all open tabs with IDs
3. select_page → switch context to a different tab
4. close_page → clean up when done
```

This enables testing flows that span multiple pages (e.g., open app in tab 1,
check admin panel in tab 2, verify email in tab 3).

---

## Device Emulation

Test responsive design and mobile behavior:

```
emulate:
  viewport: "375x812x3,mobile,touch"    # iPhone-like
  colorScheme: "dark"                      # Dark mode
  networkConditions: "Slow 3G"            # Network throttling
  geolocation: "10.8231x106.6297"        # Ho Chi Minh City
```

---

## Common Patterns

### Pattern: Form Submission Test
```
1. Navigate to form page
2. Take snapshot → identify form fields (uid of each input)
3. fill_form with all field values at once
4. Take snapshot → find submit button
5. click submit button
6. wait_for success message text
7. Take snapshot → verify success state
8. List console messages → check for errors
```

### Pattern: SPA Navigation Test
```
1. Navigate to SPA root
2. Take snapshot → find nav links
3. click link → wait_for target page content
4. Take snapshot → verify correct page loaded
5. Repeat for each route
6. Check: browser back/forward works (navigate_page type: "back"/"forward")
```

### Pattern: API Integration Test
```
1. Navigate to page that makes API calls
2. Perform the action (click button, submit form)
3. list_network_requests → find the API call
4. get_network_request → verify request/response details
5. Take snapshot → verify UI updated correctly
```

### Pattern: Visual Regression Check
```
1. Navigate to page
2. take_screenshot (save to known path)
3. Compare with previous screenshot (manual or diff tool)
4. Optionally: resize_page to different dimensions → screenshot again
5. emulate mobile → screenshot for mobile view
```

---

## Integration with Governed Workflow

```yaml
USAGE_IN_GOVERNED_WORKFLOW:
  when: Phase 4 (Testing) — for E2E smoke tests requiring auth
  trigger: Feature has authenticated UI flows or needs DevTools analysis

  workflow:
    1. Unit tests pass (Jest/Vitest) ✅
    2. Integration tests pass ✅
    3. E2E test with chrome-e2e:
       a. Verify auth flow works (Google/SSO/session)
       b. Test critical user paths through the app
       c. Run Lighthouse for accessibility/SEO
       d. Capture screenshots as evidence
       e. Check console for errors, network for failures
       f. Add results to 04_tests/tests.md

  evidence:
    - Screenshots saved to /tmp/ or docs/runs/<slug>/04_tests/screenshots/
    - Lighthouse reports in output directory
    - Console error summary
    - Network request analysis
    - Pass/fail per test scenario
```

---

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| `list_pages` returns empty | MCP server not connected | Restart VS Code, check mcp.json |
| autoConnect not working | Chrome < 144 or remote debugging not enabled | Go to `chrome://inspect/#remote-debugging` and enable |
| Google login shows CAPTCHA | Bot detection on MCP browser | Use `--autoConnect` with real Chrome instead |
| Elements not found after click | Page mutated, old uids invalid | Always take fresh snapshot after any interaction |
| Slow first response | MCP server cold start | Normal — first tool call loads the server (~5-10s) |
| `wait_for` times out | Text never appeared on page | Check spelling, try broader text, increase timeout |
| Form fill fails | Wrong uid or element not interactable | Take snapshot, verify uid is an input/select element |
