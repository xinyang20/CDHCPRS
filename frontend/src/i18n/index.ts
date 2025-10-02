import { createI18n } from "vue-i18n";
import zhCN from "../../i18n/zh-CN.json" assert { type: "json" };
import enUS from "../../i18n/en-US.json" assert { type: "json" };

export type AppLocale = "zh-CN" | "en-US";

const STORAGE_KEY = "cdhcprs_locale";
const DEFAULT_LOCALE: AppLocale = "zh-CN";

const getInitialLocale = (): AppLocale => {
  if (typeof window === "undefined") {
    return DEFAULT_LOCALE;
  }
  const stored = window.localStorage.getItem(STORAGE_KEY) as AppLocale | null;
  return stored === "zh-CN" || stored === "en-US" ? stored : DEFAULT_LOCALE;
};

export const i18n = createI18n({
  legacy: false,
  locale: getInitialLocale(),
  fallbackLocale: DEFAULT_LOCALE,
  messages: {
    "zh-CN": zhCN,
    "en-US": enUS,
  },
});

export const availableLocales: Array<{ label: string; value: AppLocale }> = [
  { label: zhCN.language.zhCN, value: "zh-CN" },
  { label: enUS.language.enUS, value: "en-US" }
];

export const setLocale = (locale: AppLocale) => {
  i18n.global.locale.value = locale;
  if (typeof window !== "undefined") {
    window.localStorage.setItem(STORAGE_KEY, locale);
  }
};

export const currentLocale = () => i18n.global.locale.value as AppLocale;
