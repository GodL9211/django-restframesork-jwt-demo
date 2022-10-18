<template>
  <div class="login-container">
    <el-form
      ref="loginForm"
      :model="state.loginForm"
      :rules="rules"
      autocomplete="on"
      class="login-form"
      label-position="left"
    >
      <div class="title-container">
        <h3 class="title">博客管理后台</h3>
      </div>

      <el-form-item prop="account">
        <el-input
          ref="account"
          v-model="state.loginForm.account"
          autocomplete="on"
          name="account"
          placeholder="Account"
          tabindex="1"
          type="text"
        />
      </el-form-item>

      <el-tooltip
        v-model="state.capsTooltip"
        content="Caps lock is On"
        manual
        placement="right"
      >
        <el-form-item prop="password">
          <el-input
            :key="state.passwordType"
            ref="password"
            v-model="state.loginForm.password"
            :type="state.passwordType"
            autocomplete="on"
            name="password"
            placeholder="Password"
            tabindex="2"
            @blur="state.capsTooltip = false"
            @keyup="checkCapslock"
            @keyup.enter="handleLogin"
          />
        </el-form-item>
      </el-tooltip>
      <p class="fp" @click="startFp">Forget password</p>

      <el-button
        :loading="state.loading"
        style="width: 100%; margin-bottom: 30px"
        type="primary"
        @click.prevent="handleLogin"
      >
        Login
      </el-button>
    </el-form>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive } from "vue";
import { forgetPassword, login } from "../../api/service";
import { SET_USER } from "../../store";
import { User } from "../../types";

export default defineComponent({
  name: "Login",
  setup() {
    const validatePassword = (rule: any, value: string, callback: Function) => {
      if (value.length < 6) {
        callback(new Error("The password can not be less than 6 digits"));
      } else {
        callback();
      }
    };
    const state = reactive({
      loginForm: {
        account: "",
        password: "",
      },

      loginRules: {
        account: [{ required: true, trigger: "blur" }],
        password: [
          {
            required: true,
            trigger: "blur",
            validator: validatePassword,
          },
        ],
      },
      forgetRules: {
        account: [{ required: true, trigger: "blur" }],
      },
      passwordType: "password",
      capsTooltip: false,
      loading: false,
      isFP: false,
    });

    return {
      state,
      validatePassword,
    };
  },
  mounted() {
    if (this.state.loginForm.account === "") {
      this.$refs.account.focus();
    } else if (this.state.loginForm.password === "") {
      this.$refs.password.focus();
    }
  },
  computed: {
    rules() {
      return this.state.isFP ? this.state.forgetRules : this.state.loginRules;
    },
  },
  methods: {
    checkCapslock(e: KeyboardEvent) {
      const { key } = e;
      this.state.capsTooltip =
        key && key.length === 1 && key >= "A" && key <= "Z";
    },
    handleLogin() {
      this.state.isFP = false;
      this.$refs.loginForm.validate(async (valid: Boolean) => {
        if (valid) {
          this.state.loading = true;
          const req = {
            username: this.state.loginForm.account,
            password: this.state.loginForm.password,
          };
          try {
            const data: any = await login(req);
            const user: User = {
              id: data.id,
              username: data.username,
              avatar: data.avatar,
              email: data.email,
              nickname: data.nickname,
              is_superuser: data.is_superuser
            };

            this.$store.commit(SET_USER, {
              user,
            });
            window.sessionStorage.userInfo = JSON.stringify(user);
            await this.$router.push({
              path: "/admin",
            });
            this.state.loading = false;
          } catch (e) {
            this.state.loading = false;
          }
        }
      });
    },
    startFp() {
      this.state.isFP = true;
      this.$refs.loginForm.clearValidate();
      this.$nextTick(() => {
        this.$refs.loginForm.validate((valid: Boolean) => {
          if (valid) {
            this.$confirm(
              "We will send a new password to " + this.state.loginForm.account,
              "Tip",
              {
                confirmButtonText: "OK",
                cancelButtonText: "Cancel",
                type: "warning",
              }
            ).then(() => {
              forgetPassword({ account: this.state.loginForm.account }).then(
                (data) => {
                  if (!data.error) {
                    this.$message({
                      message: "success!",
                      type: "success",
                      duration: 1.5 * 1000,
                    });
                  }
                }
              );
            });
          }
        });
      });
    },
  },
});
</script>

<style lang="less" scoped>
.login-container {
  min-height: 100%;
  width: 100%;
  overflow: hidden;
  background-repeat: no-repeat;
  background-position: center;
  display: flex;
  align-items: center;
  justify-content: center;
  filter: hue-rotate(200deg);
}

.login-form {
  //position: absolute;
  width: 300px;
  max-width: 100%;
  overflow: hidden;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  margin: auto;
  height: 350px;
}

.tips {
  font-size: 14px;
  color: #fff;
  margin-bottom: 10px;
}

.tips span:first-of-type {
  margin-right: 16px;
}

.svg-container {
  padding: 6px 5px 6px 15px;
  color: #889aa4;
  vertical-align: middle;
  width: 30px;
  display: inline-block;
}

.title-container {
  position: relative;
  color: #333;
}

.title-container .title {
  font-size: 40px;
  margin: 0px auto 40px auto;
  text-align: center;
  font-weight: bold;
}

.show-pwd {
  position: absolute;
  right: 10px;
  top: 7px;
  font-size: 16px;
  color: #889aa4;
  cursor: pointer;
  user-select: none;
}

.thirdparty-button {
  position: absolute;
  right: 0;
  bottom: 6px;
}

.fp {
  font-size: 12px;
  text-align: right;
  margin-bottom: 10px;
  cursor: pointer;
}
</style>