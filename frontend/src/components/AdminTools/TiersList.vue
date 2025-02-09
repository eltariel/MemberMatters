<template>
  <div>
    <q-dialog v-model="addTierDialog" persistent>
      <q-card>
        <q-card-section class="row items-center">
          <span class="q-ml-sm">{{ $t("tiers.add") }}</span>
        </q-card-section>

        <q-card-actions align="right">
          <q-form ref="formRef" @submit="submitTier()">
            <q-input
              v-model="form.name"
              outlined
              :debounce="debounceLength"
              :label="$t('form.name')"
              :rules="[
                (val) =>
                  validateNotEmpty(val) || $t('validation.cannotBeEmpty'),
              ]"
              :disable="form.success"
            />

            <q-input
              v-model="form.description"
              outlined
              :debounce="debounceLength"
              :label="$t('form.description')"
              :rules="[
                (val) =>
                  validateNotEmpty(val) || $t('validation.cannotBeEmpty'),
              ]"
              :disable="form.success"
            />

            <q-checkbox
              v-model="form.visible"
              :label="$t('form.visibleToMembers')"
            />

            <q-checkbox v-model="form.featured" :label="$t('form.featured')" />

            <q-banner
              v-if="form.success"
              class="bg-positive text-white q-my-md"
            >
              {{ $t("tierForm.success") }}
            </q-banner>

            <q-banner v-if="form.error" class="bg-negative text-white q-my-md">
              {{ $t(this.form.errorMessage || "tierForm.fail") }}
            </q-banner>

            <q-card-actions
              v-if="!form.success"
              align="right"
              class="text-primary"
            >
              <q-btn
                v-close-popup
                flat
                :label="$t('button.cancel')"
                :disable="loading"
              />
              <q-btn
                color="primary"
                :label="$t('button.submit')"
                :loading="loading"
                :disable="loading"
                type="submit"
              />
            </q-card-actions>

            <q-card-actions v-else align="right" class="text-primary">
              <q-btn
                v-close-popup
                flat
                :label="$t('button.close')"
                @click="resetForm()"
              />
            </q-card-actions>
          </q-form>
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-table
      @row-click="manageTier"
      :rows="tiers"
      :columns="[
        { name: 'name', label: 'Name', field: 'name', sortable: true },
        {
          name: 'description',
          style: 'max-width: 500px; text-overflow: ellipsis; overflow: clip;',
          label: 'Description',
          field: 'description',
        },
      ]"
      row-key="id"
      :filter="filter"
      v-model:pagination="pagination"
      :grid="$q.screen.xs"
      :no-data-label="$t('tiers.nodata')"
    >
      <template v-slot:top-right>
        <q-input
          v-model="filter"
          outlined
          dense
          debounce="300"
          placeholder="Search"
        >
          <template v-slot:append>
            <q-icon :name="icons.search" />
          </template>
        </q-input>
      </template>
      <template v-slot:top-left>
        <q-btn
          @click="addTierDialog = true"
          round
          color="primary"
          :icon="icons.addAlternative"
        >
          <q-tooltip :delay="500">{{ $t("tiers.add") }}</q-tooltip>
        </q-btn>
      </template>
    </q-table>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed } from "vue";
import { useStore } from "vuex";
import icons from "../../icons";
import formatMixin from "../../mixins/formatMixin";
import formMixin from "../../mixins/formMixin";
import { api } from "boot/axios";

export default defineComponent({
  name: "TiersList",
  mixins: [formatMixin, formMixin],
  setup() {
    const store = useStore();
    const getTiers = () => store.dispatch("adminTools/getTiers");
    const tiers = computed(() => store.getters["adminTools/tiers"]);

    getTiers();

    return {
      getTiers,
      tiers,
    };
  },
  data() {
    return {
      addTierDialog: false,
      loading: false,
      form: {
        error: false,
        errorMessage: null,
        success: false,
        name: "",
        description: "",
        visible: true,
        featured: false,
      },
      filter: "",
      pagination: {
        sortBy: "name",
        descending: true,
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        rowsPerPage: (this as any).$q.screen.xs ? 3 : 10,
      },
    };
  },
  computed: {
    icons() {
      return icons;
    },
  },
  methods: {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    manageTier(evt: InputEvent, row: any) {
      this.$router.push({ name: "manageTier", params: { planId: row.id } });
    },
    submitTier() {
      this.loading = true;

      api
        .post("/api/admin/tiers/", this.form)
        .then(() => {
          this.form.error = false;
          this.form.success = true;
          this.getTiers();
        })
        .catch((error) => {
          this.form.error = true;
          this.form.errorMessage = error.response.data.message;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    resetForm() {
      this.form = {
        error: false,
        success: false,
        errorMessage: null,
        name: "",
        description: "",
        visible: true,
        featured: false,
      };
      this.loading = false;
    },
  },
});
</script>

<style lang="sass" scoped>
@media (max-width: $breakpoint-xs-max)
  .access-list
    width: 100%
</style>
