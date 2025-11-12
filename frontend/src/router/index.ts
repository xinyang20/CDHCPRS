import { createRouter, createWebHistory } from "vue-router";
import type { RouteRecordRaw } from "vue-router";
import { ElMessage } from "element-plus";
import { i18n } from "../i18n";

import { authAPI } from "../api/auth";
import { useUserStore } from "../stores/user";

const routes: RouteRecordRaw[] = [
  {
    path: "/",
    name: "Home",
    component: () => import("../views/Home.vue"),
  },
  {
    path: "/about",
    name: "About",
    component: () => import("../views/About.vue"),
  },
  {
    path: "/login",
    name: "Login",
    component: () => import("../views/Login.vue"),
  },
  {
    path: "/register",
    name: "Register",
    component: () => import("../views/Register.vue"),
  },
  {
    path: "/chat",
    name: "Chat",
    component: () => import("../views/Chat.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/profile",
    name: "Profile",
    component: () => import("../views/Profile.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/admin",
    name: "Admin",
    component: () => import("../views/Admin.vue"),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, _from, next) => {
  const userStore = useUserStore();
  const token = localStorage.getItem("token");

  // 如果用户已登录且尝试访问登录/注册页面，重定向到首页
  if (token && (to.path === "/login" || to.path === "/register")) {
    next("/");
    return;
  }

  if (to.meta.requiresAuth && !token) {
    next("/login");
    return;
  }

  if (token && !userStore.user) {
    try {
      const { data } = await authAPI.getCurrentUser();
      userStore.setUser(data);
    } catch (error) {
      console.error("Failed to hydrate user in router guard", error);
      userStore.logout();
      next("/login");
      return;
    }
  }

  if (to.meta.requiresAdmin && !userStore.isAdmin()) {
    ElMessage.warning(i18n.global.t("messages.adminOnly"));
    next("/chat");
    return;
  }

  next();
});

export default router;
