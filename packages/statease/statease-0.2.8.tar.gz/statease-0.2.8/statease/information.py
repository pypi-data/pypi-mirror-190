class BuildInfo:

    def __init__(self, client):
        self.client = client
        self.study_type = ''
        self.subtype = ''
        self.design_type = ''
        self.design_model = ''
        self.runs = 0
        self.blocks = 0
        self.groups = 0
        self.build_time = 0
        self.center_points = 0

        result = self.client.send_payload({
            "method": "GET",
            "uri": "information/summary/build",
        })

        for k, v in result['payload'].items():
            setattr(self, k, v)


    def __str__(self):
            return """Build Information
Study Type: {study_type}
Subtype: {subtype}
Design Type: {design_type}
Design Model: {design_model}
Runs: {runs}
Blocks: {blocks}
Groups: {groups}
Build Time (ms): {build_time}
Center Points: {center_points}
Properties: {properties}""".format(
                study_type=self.study_type,
                subtype=self.subtype,
                design_type=self.design_type,
                design_model=self.design_model,
                runs=self.runs,
                blocks=self.blocks,
                groups=self.groups,
                build_time=self.build_time,
                center_points=self.center_points,
                properties=self.properties
            )


class Evaluation:

    def __init__(self, client):
        self.client = client
        result = self.client.send_payload({
            "method": "GET",
            "uri": "information/evaluation/dof",
        })

        for k, v in result['payload'].items():
            setattr(self, k, v)
    
    def __str__(self):
            return """Evaluation

Degrees of Freedom:
Blocks: {block_df}
Model: {model_df}
Residuals: {residual_df}
 Lack of Fit: {lack_of_fit}
 Pure Error: {pure_error_df}
Corr Total: {corr_total}
Run: {run}
Leverage: {leverage}
Space Type: {space_type}
Build Type: {build_type}

Model Terms
Terms {terms}
Standard Error {std_error}
VIF {vif}
Power {power}""".format(
                block_df=self.block_df,
                model_df=self.model_df,
                residual_df=self.residual_df,
                lack_of_fit=self.lack_of_fit,
                pure_error_df=self.pure_error_df,
                corr_total=self.corr_total,
                run=self.run,
                leverage=self.leverage,
                space_type=self.space_type,
                build_type=self.build_type,
                terms=self.terms,
                std_error=self.std_error,
                vif=self.vif,
                power=self.power,
            )

