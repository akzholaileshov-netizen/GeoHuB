-- GeoHub: 30 күндік жазылым (оқушыға көрсетілмейді).
-- Supabase SQL Editor-де бір рет іске қосыңыз.

CREATE TABLE IF NOT EXISTS subscriptions (
    telegram_id BIGINT PRIMARY KEY,
    status VARCHAR(20) NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'expired')),
    paid_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ,
    reminder_sent BOOLEAN NOT NULL DEFAULT false
);

CREATE INDEX IF NOT EXISTS subscriptions_expiry_idx
    ON subscriptions (status, expires_at, reminder_sent);

ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;

-- Service role ғана оқиды/жазады. anon/authenticated саясаты жоқ.

COMMENT ON TABLE subscriptions IS 'PRO жазылым мерзімі. Оқушыға "1 ай" деп айтылмайды.';
COMMENT ON COLUMN subscriptions.status IS 'active | expired';
COMMENT ON COLUMN subscriptions.paid_at IS 'Соңғы расталған төлем уақыты';
COMMENT ON COLUMN subscriptions.expires_at IS 'paid_at + 30 days';
COMMENT ON COLUMN subscriptions.reminder_sent IS '24 сағаттық ескерту жіберілді ме';
