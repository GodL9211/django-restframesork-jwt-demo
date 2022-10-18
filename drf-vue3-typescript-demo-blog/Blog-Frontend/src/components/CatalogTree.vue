<template>
  <el-drawer
      v-model="state.visible"
      :before-close="handleClose"
      direction="rtl"
      size="500px"
      title="目录管理"
      @opened="handleSearch"
  >
    <div class="drawer-content">
      <el-tree
          :data="state.catalogs"
          :expand-on-click-node="false"
          :props="defaultProps"
          default-expand-all
          node-key="id">
        <template #default="{ node, data }">
        <span class="custom-tree-node">
          <span>{{ node.label }}</span>
          <span>
            <el-dropdown trigger="click">
              <span class="el-dropdown-link">
                <i class="el-icon-more"/>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item icon="el-icon-edit">
                    <a class="more-button" @click.prevent="showEditDialog(data)">
                       修改
                    </a>
                  </el-dropdown-item>
                  <el-dropdown-item icon="el-icon-circle-plus">
                    <a class="more-button" @click.prevent="showAddDialog(data)">
                       新增
                    </a>
                  </el-dropdown-item>
                  <el-dropdown-item icon="el-icon-delete-solid">
                    <el-popconfirm :title="'确定删除【'+data.name+'】？'" cancelButtonText='取消' confirmButtonText='删除'
                                   icon="el-icon-info" iconColor="red" @confirm="remove(data)">
                      <template #reference>
                        <a class="more-button">
                          删除
                        </a>
                      </template>
                    </el-popconfirm>
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </span>
        </span>
        </template>
      </el-tree>
    </div>
  </el-drawer>
  <el-dialog v-model="state.showDialog" :title="state.dialogTitle">
    <el-form class="form" label-suffix="：" label-width="120px" size="medium">
      <el-form-item label="目录名称">
        <el-input v-model="state.catalog.name" autocomplete="off"></el-input>
      </el-form-item>
    </el-form>
    <template #footer>
        <span class="dialog-footer">
          <el-button @click="state.showDialog=false">取 消</el-button>
          <el-button :loading="state.loading" type="primary" @click="saveCatalog">保 存</el-button>
        </span>
    </template>
  </el-dialog>
</template>

<script lang="ts">
import {defineComponent, reactive} from "vue";
import {Catalog} from "../types";
import {deleteCatalog, getCatalogTree, saveCatalog} from "../api/service";
import {ElMessage} from "element-plus";

export default defineComponent({
  name: "CatalogTree",
  props: {
    visible: {
      type: Boolean,
      require: true,
    }
  },
  watch: {
    '$props.visible': {
      handler(val, oldVal) {
        if (val != oldVal) {
          this.state.visible = val
        }
      }
    }
  },
  emits: ['close',],
  setup(props) {
    const state = reactive({
      catalogs: [] as Array<Catalog>,
      visible: props.visible,
      showDialog: false,
      catalog: {} as Catalog,
      dialogTitle: '',
      loading: false,
    })

    const handleSearch = async () => {
      state.catalogs = await getCatalogTree();
    }
    const defaultProps = {
      children: 'children',
      label: 'name',
    }
    return {
      state,
      handleSearch,
      defaultProps
    }
  },
  methods: {
    handleClose() {
      this.$emit('close')
    },
    showAddDialog(data: Catalog) {
      this.state.showDialog = true
      //@ts-ignore
      this.state.catalog.id = undefined
      //@ts-ignore
      this.state.catalog.name = undefined
      this.state.catalog.parent = data.id
      this.state.dialogTitle = '新增目录'
    },
    showEditDialog(data: Catalog) {
      this.state.showDialog = true
      this.state.catalog = data
      this.state.dialogTitle = '修改目录'
    },
    async saveCatalog() {
      try {
        this.state.loading = true
        const method = this.state.catalog.id ? 'patch' : 'post'
        await saveCatalog(method, this.state.catalog)
        this.state.loading = false
        this.state.showDialog = false
        ElMessage({
          message: '保存成功',
          type: 'success'
        })
        await this.handleSearch()
      } catch (e) {
        console.error(e)
        ElMessage({
          message: '保存失败',
          type: 'error'
        })
        this.state.loading = false
      }
    },
    async remove(data: Catalog) {
      await deleteCatalog(data.id)
      ElMessage({
        message: '删除成功',
        type: 'success'
      })
      await this.handleSearch()
    }
  }

})
</script>

<style lang="less" scoped>
.drawer-content {
  padding: 12px 0 0 24px;
  border-top: #eeeeee 1px solid;
  overflow: auto;
}

.custom-tree-node {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  padding-right: 32px;
}

.add-button {
  margin-bottom: 12px;
}

</style>