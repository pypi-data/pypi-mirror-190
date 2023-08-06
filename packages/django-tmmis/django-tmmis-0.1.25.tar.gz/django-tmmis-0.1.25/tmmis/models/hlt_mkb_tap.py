import datetime

from .base_model import *


class HltMkbTap(BaseModel):
    """
    Диагнозы ТАП
    """

    id = models.AutoField(db_column="MKB_TAPID", primary_key=True)
    mkb = models.ForeignKey("OmsMkb", db_column="rf_MKBID", **FK_DEFAULT)
    tap = models.ForeignKey("HltTap", db_column="rf_TAPID", **FK_DEFAULT)
    is_main = models.BooleanField(db_column="isMain", default=False)
    comments = models.CharField(db_column="Comments", max_length=4096, default="")
    flags = models.IntegerField(db_column="FLAGS", default=0)
    registration_end_reason_id = models.IntegerField(db_column="rf_kl_RegistrationEndReasonID")
    disease_type_id = models.IntegerField(db_column="rf_kl_DiseaseTypeID", default=0)
    trauma_type_id = models.IntegerField(db_column="rf_kl_TraumaTypeID", default=0)
    disp_reg_state_id = models.IntegerField(db_column="rf_kl_DispRegStateID", default=0)
    doc_guid = models.CharField(db_column="rf_DocGUID", max_length=3636, default="00000000-0000-0000-0000-000000000000")
    doc_type_def_guid = models.CharField(
        db_column="rf_DocTypeDefGUID", max_length=36, default="00000000-0000-0000-0000-000000000000"
    )
    diagnos_type_id = models.IntegerField(db_column="rf_kl_DiagnosTypeID", default=0)
    mkb_external_id = models.IntegerField(db_column="rf_MKBExternalID", default=0)
    guid = models.UUIDField(db_column="GUID", max_length=36, default=uuid4)
    date = models.DateTimeField(db_column="Date", default=datetime.date(1900, 1, 1))
    clinical_diagnos = models.CharField(db_column="ClinicalDiagnos", max_length=2000, default="")
    is_final = models.BooleanField(db_column="IsFinal", default=False)
    doc_prvd = models.ForeignKey("HltDocPrvd", db_column="rf_DocPRVDID", **FK_DEFAULT)

    class Meta:
        managed = False
        db_table = "hlt_mkb_tap"
