# Amvera Container Startup Fixes

## Issues Fixed

### 1. **Missing Webhook Configuration Attributes** ✓
**File**: `src/bot/config.py`
- **Problem**: `app.py` referenced non-existent config attributes: `webhook_host`, `webhook_port`, `webhook_path`, `webhook_secret`
- **Solution**: Added these attributes to the `Config` class with sensible defaults:
  - `webhook_host: str = "localhost"`
  - `webhook_port: int = 443`
  - `webhook_path: str = "/webhook"`
  - `webhook_secret: str = ""`

### 2. **Incorrect Event Handler Signatures** ✓
**File**: `app.py`
- **Problem**: Event handlers had incorrect signatures:
  - `async def on_startup(bot: Bot)` - aiogram dispatcher doesn't pass bot to startup handlers
  - `async def on_shutdown(bot: Bot)` - same issue
- **Solution**: Removed parameters from handler signatures:
  - `async def on_startup()` - uses global `bot` variable
  - `async def on_shutdown()` - uses global `bot` variable

### 3. **Malformed Webhook URL Construction** ✓
**File**: `app.py`
- **Problem**: URL was constructed as `https://host:80/webhook` (port 80 with HTTPS is invalid)
- **Solution**: Added logic to handle HTTPS port 443 correctly:
  ```python
  if WEBHOOK_PORT == 443:
      WEBHOOK_URL = f"https://{WEBHOOK_HOST}{WEBHOOK_PATH}"
  else:
      WEBHOOK_URL = f"https://{WEBHOOK_HOST}:{WEBHOOK_PORT}{WEBHOOK_PATH}"
  ```

### 4. **Config Injection in Message Handler** ✓
**File**: `src/bot/routers/chatgpt.py`
- **Problem**: Handler tried to inject `config: Config` parameter:
  ```python
  async def chatgpt_handler(message: Message, config: Config) -> None:
  ```
  aiogram cannot auto-inject arbitrary dependencies like this.
- **Solution**: Load config at module level and use it directly:
  ```python
  config = load_config()
  
  async def chatgpt_handler(message: Message) -> None:
      # Uses module-level config
  ```

### 5. **Unused Groq Service with Config Error** ✓
**File**: `src/bot/services/groq_llm.py` (DELETED)
- **Problem**: Service referenced non-existent `config.groq` attribute (line 50):
  ```python
  "Authorization": f"Bearer {self.config.groq.token.get_secret_value()}"
  ```
  Only `config.amvera` exists in the Config class.
- **Solution**: Deleted the unused file since the bot uses Amvera LLM, not Groq.

## Testing Recommendations

1. **Local Testing**: Run `src/bot/main.py` with polling mode to verify the bot still works
2. **Webhook Testing**: Deploy to Amvera and verify webhook setup completes without errors
3. **Environment Variables**: Ensure `.env` has all required variables:
   - `BOT_TOKEN`
   - `AMVERA_LLM_TOKEN`
   - `CONTEXT7_API_KEY`
   - Optional: `WEBHOOK_HOST`, `WEBHOOK_PORT`, `WEBHOOK_PATH`, `WEBHOOK_SECRET`

## Entry Points

- **Local Development**: `src/bot/main.py` (polling mode)
- **Production (Amvera)**: `app.py` (webhook mode)

Both entry points now have correct configurations and should work without AttributeError or signature mismatch issues.
