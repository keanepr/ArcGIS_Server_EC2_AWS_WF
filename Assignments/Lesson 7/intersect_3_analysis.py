import arcpy
arcpy.ImportToolbox(r"@\Analysis Tools.tbx")
arcpy.analysis.Intersect(
    in_features="DBO.test_egdb #",
    out_feature_class=r"C:\Users\Administrator\Documents\ArcGIS\Projects\AWS_EC2_ArcGIS_Server\AWS_EC2_ArcGIS_Server.gdb\DBO_Intersect_3",
    join_attributes="ALL",
    cluster_tolerance=None,
    output_type="INPUT"
)
