/**
 * Күнделікті cron: 24 сағаттық ескерту + мерзімі біткендерді PRO каналдан шығару.
 *
 * Secrets: BOT_TOKEN, SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, PRO_CHANNEL_ID
 * Schedule (Dashboard → Edge Functions → Cron): 0 6 * * *
 */
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const REMINDER_TEXT =
  "⚠️ Құрметті оқушы! Сіздің GeoHub VIP базаңызды пайдалану мерзімі бітуге жақын " +
  "(1 күн қалды). Базаға шектеусіз кіру мүмкіндігін сақтап қалу және жаңартылған " +
  "жаңа сұрақтарға доступ алу үшін жазылымды ұзартуды ұмытпаңыз!";

const tg = async (token: string, method: string, payload: Record<string, unknown>) => {
  const res = await fetch(`https://api.telegram.org/bot${token}/${method}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return await res.json();
};

Deno.serve(async () => {
  const token = Deno.env.get("BOT_TOKEN") ?? "";
  const channelId = Number(Deno.env.get("PRO_CHANNEL_ID") ?? "0");
  const supabase = createClient(
    Deno.env.get("SUPABASE_URL") ?? "",
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? "",
  );

  const now = new Date();
  const in24h = new Date(now.getTime() + 24 * 60 * 60 * 1000);

  const { data: reminders, error: reminderErr } = await supabase
    .from("subscriptions")
    .select("telegram_id")
    .eq("status", "active")
    .eq("reminder_sent", false)
    .gt("expires_at", now.toISOString())
    .lte("expires_at", in24h.toISOString());

  if (reminderErr) {
    return new Response(JSON.stringify({ error: reminderErr.message }), { status: 500 });
  }

  let reminded = 0;
  for (const row of reminders ?? []) {
    await tg(token, "sendMessage", { chat_id: row.telegram_id, text: REMINDER_TEXT });
    await supabase
      .from("subscriptions")
      .update({ reminder_sent: true })
      .eq("telegram_id", row.telegram_id);
    reminded += 1;
  }

  const { data: expired, error: expireErr } = await supabase
    .from("subscriptions")
    .select("telegram_id")
    .eq("status", "active")
    .lte("expires_at", now.toISOString());

  if (expireErr) {
    return new Response(JSON.stringify({ error: expireErr.message }), { status: 500 });
  }

  let limited = 0;
  for (const row of expired ?? []) {
    await tg(token, "banChatMember", { chat_id: channelId, user_id: row.telegram_id });
    await tg(token, "unbanChatMember", { chat_id: channelId, user_id: row.telegram_id });
    await supabase
      .from("subscriptions")
      .update({ status: "expired" })
      .eq("telegram_id", row.telegram_id);
    limited += 1;
  }

  return new Response(JSON.stringify({ ok: true, reminded, limited }), {
    headers: { "Content-Type": "application/json" },
  });
});
