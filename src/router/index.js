import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/about',
    name: 'about',
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue'),
    meta: {
      mainNavShow: true,
    },
  },
  {
    path: '/',
    name: 'login',
    component: () => import(/* webpackChunkName: "about" */ '../views/login/LoginView.vue'),
    meta: {
      // requireNotAuth: true,
      mainNavShow: false,
    },
  },
  {
    path: '/register',
    name: 'register',
    component: () => import(/* webpackChunkName: "about" */ '../views/login/RegisterView.vue'),
    meta: {
      // requireNotAuth: true,
      mainNavShow: false,
    },
  },
  {
    path: '/profile',
    name: 'profile',
    component: () => import('../views/login/ProfileView.vue'),
    meta: {
      mainNavShow: true,
    },
  },
  {
    path: '/projectmanage',
    name: 'projectmanage',
    component: () => import('../views/project/ProjectManage.vue'),
    meta: {
      // requireNotAuth: true,
      mainNavShow: true,
    },
  },
  {
    path: '/chat',
    name: 'chat',
    component: () => import('../views/chat/ChatView.vue'),
    meta: {
      // requireNotAuth: true,
      mainNavShow: true,
    },
  },
  {
    path: '/team',
    name: 'team',
    component: () => import('../views/team/TeamView.vue'),
    meta: {
      // requireNotAuth: true,
      mainNavShow: true,
    },
  },
  {
    path: '/design',
    name: 'design',
    component: () => import('@/views/design/DesignView.vue'),
    meta: {
      // requireNotAuth: true,
      mainNavShow: true,
    },
  },
  {
    path: '/editor',
    name: 'editor',
    //component: () => import('../../public/tinymce/FileEditor.vue'),
    component: () => import('../views/TipTapEditor.vue'),
    meta: {
      // requireNotAuth: true,
      mainNavShow: true,

    },
  },
  {
    path: '/editortable',
    name: 'editortable',
    //component: () => import('../../public/tinymce/FileEditor.vue'),
    component: () => import('../views/TableEditor.vue'),
    meta: {
      // requireNotAuth: true,
      mainNavShow: true,
    },
  },
  {
    path: '/draw',
    name: 'draw',
    //component: () => import('../../public/tinymce/FileEditor.vue'),
    component: () => import('../views/drawing/IndexP.vue'),
    meta: {
      // requireNotAuth: true,
      mainNavShow: true,

    },
  },
  /*{
    path: '/editor',
    name: 'editor',
    component: () => import('@/views/project/ProjectEditor.vue'),
    meta: {
      // requireNotAuth: true,
      mainNavShow: true,
    },
  }*/
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
