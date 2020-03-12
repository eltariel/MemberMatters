import icons from '../icons';

const PageAndRouteConfig = [
  {
    icon: icons.login, // specify the icon to use
    to: '/', // specify the URL route for this page
    name: 'rootIndex', // specify the name of this URL route
    loggedIn: false, // only allow access to logged in users if true or logged out users if false
    hiddenMenu: true, // adds the route and page config, but don't show in the menu
    component: () => import('pages/Login.vue'), // which component to load as the page
  },
  {
    icon: icons.dashboard,
    to: '/dashboard',
    name: 'dashboard',
    loggedIn: true,
    component: () => import('pages/Dashboard.vue'),
  },
  {
    icon: icons.webcams,
    to: '/webcams',
    name: 'webcams',
    loggedIn: true,
    component: () => import('pages/Webcams.vue'),
  },
  {
    icon: icons.tools,
    name: 'memberTools',
    loggedIn: true,
    children: [
      {
        icon: icons.reportIssue,
        to: '/tools/issue',
        name: 'reportIssue',
      },
      {
        icon: icons.submitProxy,
        to: '/tools/proxy',
        name: 'submitProxy',
      },
      {
        icon: icons.recentSwipes,
        to: '/tools/swipes/recent',
        name: 'recentSwipes',
      },
      {
        icon: icons.lastSeen,
        to: '/tools/swipes/lastseen',
        name: 'lastSeen',
        component: () => import('pages/LastSeen.vue'),
      },
    ],
  },
  {
    icon: icons.membership,
    name: 'membership',
    loggedIn: true,
    children: [
      {
        icon: icons.profile,
        to: '/account/profile',
        name: 'profile',
      },
      {
        icon: icons.checkAccess,
        to: '/account/access',
        name: 'checkAccess',
        component: () => import('pages/CheckAccess.vue'),
      },
      {
        icon: icons.memberbucks,
        to: '/account/memberbucks',
        name: 'manageMemberbucks',
      },
    ],
  },
  {
    icon: icons.signout,
    to: '/logout',
    name: 'logout',
    loggedIn: true,
    component: () => import('pages/Logout.vue'),
  },
  {
    icon: icons.signin,
    to: '/login',
    name: 'login',
    loggedIn: false,
    component: () => import('pages/Login.vue'),
  },
  {
    icon: icons.register,
    to: '/register',
    name: 'register',
    loggedIn: false,
  },
];

export default PageAndRouteConfig;
