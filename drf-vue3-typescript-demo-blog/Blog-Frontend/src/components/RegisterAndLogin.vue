<template>
  <el-dialog
    title="登录"
    width="40%"
    v-model="state.dialogModal"
    @close="cancel"
    :show-close="true"
  >
    <el-form>
      <el-formItem label="账号" :label-width="state.formLabelWidth">
        <el-input
          v-model="state.params.username"
          placeholder="请输入有效邮箱"
          autocomplete="off"
        />
      </el-formItem>
      <el-formItem label="密码" :label-width="state.formLabelWidth">
        <el-input
          type="password"
          placeholder="密码"
          v-model="state.params.password"
          autocomplete="off"
        />
      </el-formItem>
      <el-formItem
        v-if="isRegister"
        label="昵称"
        :label-width="state.formLabelWidth"
      >
        <el-input
          v-model="state.params.nickname"
          placeholder="用户名或昵称"
          autocomplete="off"
        />
      </el-formItem>
      <el-formItem
        v-if="isRegister"
        label="手机"
        :label-width="state.formLabelWidth"
      >
        <el-input
          v-model="state.params.phone"
          placeholder="手机号"
          autocomplete="off"
        />
      </el-formItem>
      <el-formItem
        v-if="isRegister"
        label="简介"
        :label-width="state.formLabelWidth"
      >
        <el-input
          v-model="state.params.desc"
          placeholder="个人简介"
          autocomplete="off"
        />
      </el-formItem>
    </el-form>
    <template v-slot:footer>
      <div class="dialog-footer">
        <el-button
          v-if="isLogin"
          :loading="state.btnLoading"
          type="primary"
          @click="handleOk"
        >
          登 录
        </el-button>
        <el-button
          v-if="isRegister"
          :loading="state.btnLoading"
          type="primary"
          @click="handleOk"
          >注 册
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script lang="ts">
import { defineComponent, reactive, watch } from "vue";
import { useStore } from "vuex";
import { ElMessage } from "element-plus";
import { SET_USER, StateKey } from "../store";
import { login, register } from "../api/service";
import { User } from "../types";

export default defineComponent({
  name: "RegisterAndLogin",
  props: {
    visible: {
      type: Boolean,
      default: false,
    },
    handleFlag: {
      type: String,
      default: false,
    },
  },
  computed: {
    isLogin(): Boolean {
      return this.handleFlag === "login";
    },
    isRegister(): Boolean {
      return this.handleFlag === "register";
    },
  },
  emits: ["ok", "cancel"],
  setup(props, context) {
    const store = useStore(StateKey);
    const state = reactive({
      dialogModal: props.visible,
      btnLoading: false,
      loading: false,
      formLabelWidth: "60px",
      params: {
        email: "",
        username: "",
        nickname: "",
        password: "",
        phone: "",
        desc: "",
      },
    });

    const submit = async (): Promise<void> => {
      let data: any = "";
      state.btnLoading = true;
      try {
        if (props.handleFlag === "register") {
          state.params.email = state.params.username;
          data = await register(state.params);
        } else {
          data = await login(state.params);
        }
        state.btnLoading = false;

        const user: User = {
          id: data.id,
          username: data.username,
          avatar: data.avatar,
          email: data.email,
          nickname: data.nickname,
        };
        store.commit(SET_USER, {
          user,
        });
        window.sessionStorage.userInfo = JSON.stringify(user);
        context.emit("ok", false);
        ElMessage({
          message: "操作成功",
          type: "success",
        });
        state.dialogModal = false;
      } catch (e) {
        console.error(e);
        state.btnLoading = false;
      }
    };

    const handleOk = (): void => {
      const reg = new RegExp(
        "^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$"
      ); //正则表达式
      if (!state.params.username) {
        ElMessage({
          message: "账号不能为空！",
          type: "warning",
        });
        return;
      } else if (!reg.test(state.params.username)) {
        ElMessage({
          message: "请输入格式正确的邮箱！",
          type: "warning",
        });
        return;
      }
      if (props.handleFlag === "register") {
        if (!state.params.password) {
          ElMessage({
            message: "密码不能为空！",
            type: "warning",
          });
          return;
        } else if (!state.params.nickname) {
          ElMessage({
            message: "昵称不能为空！",
            type: "warning",
          });
          return;
        }
        const re = /^(((13[0-9])|(15[0-9])|(17[0-9])|(18[0-9]))+\d{8})$/;
        if (state.params.phone && !re.test(state.params.phone)) {
          ElMessage({
            message: "请输入正确的手机号!",
            type: "warning",
          });
          return;
        }
      }
      submit();
    };

    const cancel = (): boolean => {
      context.emit("cancel", false);
      return false;
    };

    watch(props, (val, oldVal) => {
      state.dialogModal = val.visible;
    });

    return {
      state,
      handleOk,
      submit,
      cancel,
    };
  },
});
</script>
<style scoped>
.dialog-footer {
  text-align: right;
}
</style>