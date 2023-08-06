# Example running a custom job on the brevettiai platform
from pydantic import Field

from brevettiai.platform import PlatformAPI, Job, JobSettings
from brevettiai.data.image.bcimg_dataset import BcimgDatasetSamples
from brevettiai.interfaces.pivot import export_pivot_table
from brevettiai.datamodel import ImageAnnotation
from brevettiai.io.files import load_files


class ApplicationExplorationSettings(JobSettings):
    """Class containing all the custom parameters for the job"""
    data: BcimgDatasetSamples = Field(default_factory=BcimgDatasetSamples)


class ApplicationExploration(Job):
    """Class for running the actual job, specifying which parameter set to use"""
    settings: ApplicationExplorationSettings

    def get_samples(self):
        all_sequences = self.settings.data.get_sequences(self.datasets)
        assert all_sequences.empty is False, "Datasets must contain at least 1 sequence"

        is_annotated_mask = ~all_sequences.annotation_frames.isna()
        annotated_sequences = all_sequences[is_annotated_mask]

        annotated_samples = self.settings.data.expand_sequences_with_annotations(annotated_sequences)

        annotations = dict(load_files(paths=annotated_samples.annotation_path.unique(),
                                      callback=lambda pth, x: (pth, ImageAnnotation.parse_raw(x)),
                                      io=self.io, cache=False))

        samples = self.settings.data.expand_annotations_files(annotated_samples, annotations)
        # TODO Inside  points, bbox
        return samples

    def build_pivot(self, samples):
        fields = {
            "category": "Annotation",
            "label": "Folder",
            "dataset_id": {
                "label": "Dataset id",
                "sort": [x.id for x in sorted(self.datasets, key=lambda x: x.name)]
            }
        }

        tags = self.backend.get_root_tags(self.id, self.api_key)
        export_pivot_table(self.artifact_path("pivot", dir=True), samples, fields,
                           datasets=self.datasets, tags=tags, rows=["dataset_id"], cols=["label"])

    def run(self):
        settings = self.settings

        # Read dataset
        samples = self.get_samples()

        # Build exports
        self.build_pivot(samples)


def main(application="0ca047b5-9b33-4928-9065-1ec05ab3ee75"):
    platform = PlatformAPI()
    platform.run_experiment(
        name="exploration",
        job_type=ApplicationExploration,
        settings=ApplicationExplorationSettings(parameter=42),
        application=application,
    )


if __name__ == "__main__":
    main()
