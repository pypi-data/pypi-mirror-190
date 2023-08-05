import pandas as pd
import numpy as np
import plotly.express as px
from IPython.display import display

from dqfit.services import Query
from dqfit.preprocessing import BundleFramer
from dqfit.categories import Complete, Conformant, Plausible


class DQIModel:
    def __init__(self, in_dir: str, out_dir=False, context=[]):
        self.in_dir: str = in_dir
        self.out_dir: str = out_dir
        self.context: list = context
        self.context_path: pd.Series = self._load_context_path()
        self.results: pd.DataFrame = self.fit()
        self.index = self._get_index()
        self.patient_level = self._patient_level_matrix()
        self.fhir_path_summary = self._fhir_path_summary()
        if out_dir:
            self._handle_out()

    def visualize(self):
        print(f"Index: {self.index}")
        display(self.results)
        display(self.fhir_path_summary)
        self._visualize_fhir_path_summary().show(renderer="notebook")

    def fit(self) -> pd.DataFrame:
        bundles = Query.bundles_query(self.in_dir)
        # add tdqm?
        bundles["fhir_path"] = bundles.apply(self._score_fhir_path, axis=1)
        bundles["patient_level_score"] = bundles["fhir_path"].apply(
            self._score_patient_level
        )
        print(f"Processed {len(bundles)} bundles")
        return bundles

    def _get_index(self):
        index = int(self.results["patient_level_score"].sum().sum())
        return index

    def _load_context_path(self) -> pd.Series:
        # WIP
        context = Query.ig_struct_query(
            resource_types=["Patient", "Condition", "Procedure", "Observation"],
            must_support=True,
        )
        return context["path"]

    def _score_fhir_path(self, bundle: pd.Series) -> pd.DataFrame:
        """
        A FHIR Path is...
        Patient.birthDate
        Patient.telecom
        Observation.status

        For each Path in the Bundle and in the Context,
        assign score per category
        """
        fhir_path = BundleFramer.fhir_path_frame(bundle)
        fhir_path = fhir_path[fhir_path["path"].isin(self.context_path)].reset_index(
            drop=True
        )
        fhir_path["conformant"] = fhir_path.apply(Conformant.score, axis=1)
        fhir_path["complete"] = fhir_path.apply(Complete.score, axis=1)
        fhir_path["plausible"] = fhir_path.apply(Plausible.score, axis=1)
        return fhir_path

    def _handle_out(self):
        result_vectors = ["bundle_index", "fhir_path", "patient_level_score"]
        df = self.results[result_vectors].reset_index(drop=True)
        df["fhir_path"] = df["fhir_path"].apply(lambda x: x.to_dict(orient="records"))
        df.to_json(f"{self.out_dir}/results.json", orient="records")
        fig = self._visualize_fhir_path_summary()
        fig.write_html(f"{self.out_dir}/fhir_path_summary.html")

    @staticmethod
    def _score_patient_level(fhir_path: pd.Series) -> np.array:
        return np.array(
            [
                fhir_path["conformant"].mean(),
                fhir_path["complete"].mean(),
                fhir_path["plausible"].mean(),
            ]
        )

    def _patient_level_matrix(self):
        return pd.DataFrame(
            dict(
                conformant=self.results["patient_level_score"][0],
                plausible=self.results["patient_level_score"][1],
                complete=self.results["patient_level_score"][2],
            )
        )

    def fhir_path_matrix(self):
        return pd.concat(list(self.results["fhir_path"]))

    def _fhir_path_summary(self):
        cohort_fhir_path = self.fhir_path_matrix()
        fhir_path_summary = cohort_fhir_path.groupby(["resourceType", "path"]).agg(
            document_count=("bundle_index", "nunique"),
            term_count=("path", "count"),
            conformant=("conformant", "mean"),
            complete=("complete", "mean"),
            plausible=("plausible", "mean"),
        )
        # fhir_path_summary

        return fhir_path_summary.reset_index()

    def _visualize_fhir_path_summary(self):
        df = self.fhir_path_summary.melt(
            id_vars=["resourceType", "path", "document_count", "term_count"]
        )
        fig = px.scatter(
            df,
            y="path",
            x="value",
            facet_col="variable",
            title=f"Index: {self.index} | n={len(self.results)} | Context {self.context}",
            hover_data=["document_count", "term_count"],
            color="resourceType",
            height=600,
        )
        return fig