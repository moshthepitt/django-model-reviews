# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestForms::test_model_review_formset 1'] = '''<input type="hidden" name="form-TOTAL_FORMS" value="3" id="id_form-TOTAL_FORMS"><input type="hidden" name="form-INITIAL_FORMS" value="0" id="id_form-INITIAL_FORMS"><input type="hidden" name="form-MIN_NUM_FORMS" value="0" id="id_form-MIN_NUM_FORMS"><input type="hidden" name="form-MAX_NUM_FORMS" value="3" id="id_form-MAX_NUM_FORMS">
<tr><th><label for="id_form-0-review_status">Status:</label></th><td><select name="form-0-review_status" id="id_form-0-review_status">
  <option value="1">Approved</option>

  <option value="3">Pending</option>

  <option value="2">Rejected</option>

</select><input type="hidden" name="form-0-review" value="1338" id="id_form-0-review"><input type="hidden" name="form-0-reviewer" value="1338" id="id_form-0-reviewer"></td></tr> <tr><th><label for="id_form-1-review_status">Status:</label></th><td><select name="form-1-review_status" id="id_form-1-review_status">
  <option value="1">Approved</option>

  <option value="3">Pending</option>

  <option value="2">Rejected</option>

</select><input type="hidden" name="form-1-review" value="1339" id="id_form-1-review"><input type="hidden" name="form-1-reviewer" value="1339" id="id_form-1-reviewer"></td></tr> <tr><th><label for="id_form-2-review_status">Status:</label></th><td><select name="form-2-review_status" id="id_form-2-review_status">
  <option value="1">Approved</option>

  <option value="3">Pending</option>

  <option value="2">Rejected</option>

</select><input type="hidden" name="form-2-review" value="1340" id="id_form-2-review"><input type="hidden" name="form-2-reviewer" value="1340" id="id_form-2-reviewer"></td></tr>'''
