import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import LogIn from '@/components/LogIn'
import Menu from '@/components/Menu'
import Vis from '@/components/Vis'
import ResultLt from '@/components/ResultLt'
import Result from '@/components/Result'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path:'/login',
      component:LogIn
    },
    {
      path:'/menu',
      component:Menu
    },
    {
      path:'/vis',
      name:'Vis',
      component:Vis
    },
    {
      path:'/resultlt',
      name:'ResultLt',
      component:ResultLt
    },
    {
      path:'/result',
      name:'Result',
      component:Result
    },

  ]
})
