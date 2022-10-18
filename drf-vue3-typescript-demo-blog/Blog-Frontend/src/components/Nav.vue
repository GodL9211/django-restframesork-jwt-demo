<template>
  <div class="nav">
    <div class="nav-content">
      <el-row :gutter="20">
        <el-col :span="3">
          <router-link to="/">
            <img class="logo" src="../assets/logo.jpeg" alt="微谈小智" />
          </router-link>
        </el-col>
        <el-col :span="16">
          <el-menu
            :default-active="navIndex"
            :router="true"
            active-text-color="#409EFF"
            class="el-menu-demo"
            mode="horizontal"
          >
            <el-menuItem
              v-for="r in navs"
              :key="r.index"
              :index="r.index"
              :route="r.path"
            >
              {{ r.name }}
            </el-menuItem>
          </el-menu>
        </el-col>
        <el-col v-if="isLogin" :span="5">
          <div class="nav-right">
            <el-dropdown>
              <span class="el-dropdown-link">
                {{ userInfo.nickname ? userInfo.nickname : userInfo.username
                }}<i class="el-icon-arrow-down el-icon--right"></i>
              </span>
              <img
                v-if="!userInfo.avatar"
                alt="微谈小智"
                class="user-img"
                src="../assets/user.png"
              />
              <img
                v-if="userInfo.avatar"
                :src="userInfo.avatar"
                alt="微谈小智"
                class="user-img"
              />
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="handleClick"
                    >登 出</el-dropdown-item
                  >
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-col>
        <el-col v-else :span="4">
          <div class="nav-right" v-if="!isLogin">
            <el-button
              size="small"
              type="primary"
              @click="handleClick('login')"
            >
              登 录</el-button
            >
            <el-button
              size="small"
              type="danger"
              @click="handleClick('register')"
            >
              注 册
            </el-button>
          </div>
          <RegisterAndLogin
            :handle-flag="state.handleFlag"
            :visible="state.visible"
          />
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive } from "vue";
import { User } from "../types";
import { useStore } from "vuex";
import { CLEAR_USER, SET_NAV_INDEX, StateKey } from "../store";
import RegisterAndLogin from "./RegisterAndLogin.vue";
import { logout } from "../api/service";

export default defineComponent({
  name: "Nav",
  components: { RegisterAndLogin },
  computed: {
    userInfo(): User {
      const store = useStore(StateKey);
      return store.state.user;
    },
    isLogin(): Boolean {
      return this.userInfo.id > 0;
    },
    navs(){
      const store = useStore(StateKey);
      return store.state.navs;
    },
    navIndex() {
      const store = useStore(StateKey);
      return store.state.navIndex;
    },
  },
  watch: {
    $route: {
      handler(val: any, oldVal: any) {
        this.routeChange(val, oldVal);
      },
      immediate: true,
    },
  },
  setup() {
    const state = reactive({
      handleFlag: "",
      visible: false,
      title: "主页",
    });

    const store = useStore(StateKey);

    const routeChange = (newRoute: any, oldRoute: any): void => {
      for (let i = 0; i < store.state.navs.length; i++) {
        const l = store.state.navs[i];
        if (l.path === newRoute.path) {
          state.title = l.name;
          store.commit(SET_NAV_INDEX, l.index);
          return;
        }
      }
      store.commit(SET_NAV_INDEX, "-1");
    };

    const handleClick = async (route: string) => {
      if (["login", "register"].includes(route)) {
        state.handleFlag = route;
        state.visible = true;
      } else {
        await logout();
        window.sessionStorage.userInfo = "";
        store.commit(CLEAR_USER);
      }
    };

    return {
      state,
      handleClick,
      routeChange,
    };
  },
});
</script>

<style lang="less">
.nav {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1000;
  width: 100%;
  border-bottom: 1px solid #eee;
  background-color: #fff;

  .nav-content {
    width: 1200px;
    margin: 0 auto;
  }

  .logo {
    height: 50px;
    margin: 0;
    border-radius: 50%;
    margin-top: 5px;
  }

  .el-menu.el-menu--horizontal {
    border-bottom: none;
  }

  .el-menu--horizontal > .el-menu-item {
    cursor: pointer;
    color: #333;
  }

  .nav-right {
    position: relative;
    padding-top: 15px;
    text-align: right;

    .el-dropdown {
      cursor: pointer;
      padding-right: 60px;
    }

    .user-img {
      position: absolute;
      top: -15px;
      right: 0;
      width: 50px;
      border-radius: 50%;
    }
  }
}

</style>