# defines functions for transforming data between educelab.mets and gui

from typing import Union, Any

from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem
from PySide6.QtWidgets import QListWidgetItem

from educelab import mets
from educelab.mets_gui import constants
from educelab.mets_gui.utils import CustomListItem, make_item


# section dedicated to transforming data between major mets sections and
# gui tabs
# ----------------------------------------------------------------------
def struct_map_from_xml(data: list[mets.StructuralMap]) -> list[
    CustomListItem]:
    struct_maps = []
    for struct_map in data:
        values = {}
        values[constants.Attributes.ID.value] = get_data(struct_map.id)
        values[constants.Attributes.TYPE.value] = get_data(struct_map.type)
        values[constants.Attributes.LABEL.value] = get_data(struct_map.label)
        values[
            constants.Labels.TAG.value] = constants.ElementTags.STRUCT_MAP.value

        values[constants.Labels.OTHER_ATTRIBS.value] = process_other_attribs(
            struct_map.other_attribs)

        item = make_item(values)

        root = struct_map.div
        item.model.appendRow(process_struct_map(root))

        struct_maps.append(item)

    return struct_maps


def struct_map_to_xml(data: list[CustomListItem]) -> list[
    mets.StructuralMap]:
    struct_maps = []
    for item in data:
        item_data = item.data(Qt.ItemDataRole.UserRole)
        div = transform_struct_map(item.model.item(0))
        other_attribs = transform_other_attribs(
            item_data[constants.Labels.OTHER_ATTRIBS.value])
        struct_maps.append(
            mets.StructuralMap(div=div,
                               element_id=pass_data(item_data[
                                                        constants.Attributes.ID.value]),
                               label=pass_data(item_data[
                                                   constants.Attributes.LABEL.value]),
                               struct_map_type=pass_data(item_data[
                                                             constants.Attributes.TYPE.value]),
                               other_attribs=other_attribs
                               ))
    return struct_maps


def file_sec_from_xml(data: mets.FileSection) -> Union[
    None, tuple[dict, list]]:
    if not data:
        return None
    values = {constants.Attributes.ID.value: get_data(data.id)}
    file_section_elements = []
    for child in data.file_groups:
        element = process_file_elements(child)
        file_section_elements.append(element)

    return values, file_section_elements


def file_sec_to_xml(data: tuple[dict, list]) -> mets.FileSection:
    file_section = None
    file_groups = []
    values = data[0]
    items = data[1]

    if items:
        for item in items:
            file_groups.append(transform_file_element(item))

        file_section = mets.FileSection(file_groups=file_groups,
                                        element_id=pass_data(values[
                                                                 constants.Attributes.ID.value]),
                                        other_attribs=None)

    return file_section


def header_from_xml(data: mets.Header) -> Union[
    None, tuple[dict, list, list, dict]]:
    if not data:
        return None

    values = {}
    agents = []
    alt_record_ids = []
    mets_document_id = {}

    values[constants.Attributes.ID.value] = get_data(data.id)
    values[constants.Attributes.ADMID.value] = get_data(data.admid)
    values[constants.Attributes.CREATE_DATE.value] = get_data(data.create_date)
    values[constants.Attributes.LAST_MOD_DATE.value] = get_data(
        data.last_mod_date)
    values[constants.Attributes.RECORD_STATUS.value] = get_data(
        data.record_status)

    for agent in data.agents:
        agt = {}
        agt[constants.Attributes.ID.value] = get_data(agent.id)
        agt[constants.Attributes.ROLE.value] = get_data(agent.role)
        agt[constants.Attributes.OTHER_ROLE.value] = get_data(agent.role_other)
        agt[constants.Attributes.TYPE.value] = get_data(agent.type)
        agt[constants.Attributes.OTHER_TYPE.value] = get_data(agent.type_other)
        agt[constants.Attributes.NAME.value] = get_data(agent.name.name)
        agt[constants.Attributes.NOTE.value] = []
        agt[constants.Labels.TAG.value] = agent.tag()

        agent_item = make_item(agt)

        for note in agent.notes:
            nt = []
            nt[constants.Labels.VALUE.value] = note.note
            nt[constants.Labels.TAG.value] = note.tag()

            agt[constants.Attributes.NOTE.value].append(nt)

        agents.append(agent_item)

    for alt_record_id in data.alternative_ids:
        ari = {}
        ari[constants.Attributes.ID.value] = get_data(alt_record_id.id)
        ari[constants.Attributes.TYPE.value] = get_data(alt_record_id.type)
        ari[constants.Labels.VALUE.value] = get_data(alt_record_id.value)
        ari[constants.Labels.TAG.value] = alt_record_id.tag()

        item = make_item(ari)

        alt_record_ids.append(item)

    if data.document_id:
        mets_document_id[constants.Attributes.ID.value] = get_data(
            data.document_id.id)
        mets_document_id[constants.Attributes.TYPE.value] = get_data(
            data.document_id.type)
        mets_document_id[constants.Labels.VALUE.value] = get_data(
            data.document_id.value)

    return values, agents, alt_record_ids, mets_document_id


def header_to_xml(data: tuple[dict, list[dict], list[dict]]) -> mets.Header:
    values = data[0]
    agents = data[1]
    alt_ids = data[2]
    document_id_data = values.pop(constants.Attributes.METS_DOCUMENT_ID.value)

    if any(values.values()) or agents or alt_ids or any(
            document_id_data.values()):
        agent_elements = []
        for agent in agents:
            notes = []
            for note in agent[constants.Attributes.NOTE.value]:
                notes.append(
                    mets.Note(note=note[constants.Labels.VALUE.value]))
            agent_elements.append(mets.Agent(name=mets.Name(
                pass_data(agent[constants.Attributes.NAME.value])),
                role=pass_data(agent[
                                   constants.Attributes.ROLE.value]),
                element_id=pass_data(agent[
                                         constants.Attributes.ID.value]),
                role_other=pass_data(agent[
                                         constants.Attributes.OTHER_ROLE.value]),
                agent_type=pass_data(agent[
                                         constants.Attributes.TYPE.value]),
                type_other=pass_data(agent[
                                         constants.Attributes.OTHER_TYPE.value]),
                notes=notes
            ))

        alt_id_elements = []
        for alt_id in alt_ids:
            alt_id_elements.append(
                mets.AlternativeIdentifier(
                    value=pass_data(alt_id[constants.Labels.VALUE.value]),
                    element_id=pass_data(alt_id[constants.Attributes.ID.value]),
                    ai_type=pass_data(alt_id[constants.Attributes.TYPE.value])))

        if any(document_id_data.values()):
            document_id = mets.METSDocumentID(
                value=pass_data(document_id_data[constants.Labels.VALUE.value]),
                element_id=pass_data(
                    document_id_data[constants.Attributes.ID.value]),
                id_type=pass_data(
                    document_id_data[constants.Attributes.TYPE.value]))
        else:
            document_id = None

        header = mets.Header(
            element_id=pass_data(values[constants.Attributes.ID.value]),
            admid=pass_data(values[constants.Attributes.ADMID.value]),
            create_date=pass_data(
                values[constants.Attributes.CREATE_DATE.value]),
            last_mod_date=pass_data(
                values[constants.Attributes.LAST_MOD_DATE.value]),
            record_status=pass_data(
                values[constants.Attributes.RECORD_STATUS.value]),
            agents=agent_elements,
            alternative_ids=alt_id_elements,
            document_id=document_id
        )
    else:
        header = None
    return header


def metadata_from_xml(amd_data: list[mets.AdministrativeMetadataSection],
                      dmd_data: list[mets.DescriptiveMetadataSection]) -> \
        list[CustomListItem]:
    metadata = []

    for amd in amd_data:
        new_id = get_data(amd.id)
        values = {constants.Attributes.ID.value: new_id,
                  constants.Labels.TAG.value: amd.tag()}
        amd_item = CustomListItem(constants.Labels.GENERIC_TAG.value % (
            values[constants.Labels.TAG.value],
            values[constants.Attributes.ID.name]))
        amd_item.setData(Qt.ItemDataRole.UserRole, values)

        for child in amd.content:
            data = {}
            data[constants.Attributes.ID.value] = get_data(child.id)
            data[constants.Attributes.GROUP_ID.value] = get_data(child.group_id)
            data[constants.Attributes.ADMID.value] = get_data(child.admid)
            data[constants.Attributes.CREATED.value] = get_data(child.created)
            data[constants.Attributes.STATUS.value] = get_data(child.status)
            data[constants.Labels.TAG.value] = child.tag()

            child_item = make_item(data)

            if child.mdref:
                child_data = {}
                child_data[constants.Attributes.ID.value] = get_data(
                    child.mdref.id)
                child_data[constants.Attributes.MIMETYPE.value] = get_data(
                    child.mdref.mimetype)
                child_data[constants.Attributes.LABEL.value] = get_data(
                    child.mdref.label)
                child_data[constants.Attributes.LOCTYPE.value] = get_data(
                    child.mdref.loctype)
                child_data[constants.Attributes.OTHER_LOCTYPE.value] = get_data(
                    child.mdref.other_loctype)
                child_data[constants.Attributes.MD_TYPE.value] = get_data(
                    child.mdref.mdtype)
                child_data[constants.Attributes.MD_TYPE_OTHER.value] = get_data(
                    child.mdref.other_mdtype)
                child_data[
                    constants.Attributes.MD_TYPE_VERSION.value] = get_data(
                    child.mdref.mdtype_version)
                child_data[constants.Attributes.SIZE.value] = get_data(
                    child.mdref.size)
                child_data[constants.Attributes.CREATED.value] = get_data(
                    child.mdref.created)
                child_data[constants.Attributes.CHECKSUM.value] = get_data(
                    child.mdref.checksum)
                child_data[constants.Attributes.CHECKSUM_TYPE.value] = get_data(
                    child.mdref.checksum_type)
                child_data[constants.Attributes.XPTR.value] = get_data(
                    child.mdref.xptr)
                child_data[constants.Attributes.XLINK_ROLE.value] = get_data(
                    child.mdref.xlink_role)
                child_data[constants.Attributes.XLINK_ARCROLE.value] = get_data(
                    child.mdref.xlink_arcrole)
                child_data[constants.Attributes.XLINK_TITLE.value] = get_data(
                    child.mdref.xlink_title)
                child_data[constants.Attributes.XLINK_ACTUATE.value] = get_data(
                    child.mdref.xlink_actuate)
                child_data[constants.Attributes.XLINK_HREF.value] = get_data(
                    child.mdref.xlink_href)
                child_data[constants.Attributes.XLINK_SHOW.value] = get_data(
                    child.mdref.xlink_show)
                child_data[constants.Labels.TAG.value] = child.mdref.tag()

                item = make_item(child_data)
                child_item.appendRow(item)

            if child.mdwrap:
                child_data = {}
                child_data[constants.Attributes.ID.value] = get_data(
                    child.mdwrap.id)
                child_data[constants.Attributes.MIMETYPE.value] = get_data(
                    child.mdwrap.mimetype)
                child_data[constants.Attributes.LABEL.value] = get_data(
                    child.mdwrap.label)
                child_data[constants.Attributes.MD_TYPE.value] = get_data(
                    child.mdwrap.mdtype)
                child_data[constants.Attributes.MD_TYPE_OTHER.value] = get_data(
                    child.mdwrap.other_mdtype)
                child_data[
                    constants.Attributes.MD_TYPE_VERSION.value] = get_data(
                    child.mdwrap.mdtype_version)
                child_data[constants.Attributes.SIZE.value] = get_data(
                    child.mdwrap.size)
                child_data[constants.Attributes.CREATED.value] = get_data(
                    child.mdwrap.created)
                child_data[constants.Attributes.CHECKSUM.value] = get_data(
                    child.mdwrap.checksum)
                child_data[constants.Attributes.CHECKSUM_TYPE.value] = get_data(
                    child.mdwrap.checksum_type)
                child_data[constants.Labels.TAG.value] = child.mdwrap.tag()

                if child.mdwrap.wrapped_data.tag() == mets.constants.ElementTags.XML_DATA.value:
                    child_data[
                        constants.Attributes.TYPE.value] = constants.DataContentTypes.XML.value
                    child_data[
                        constants.Labels.CONTENT.value] = child.mdwrap.wrapped_data.xml_string()
                else:
                    child_data[
                        constants.Attributes.ID.value] = constants.DataContentTypes.BIN.value
                    child_data[
                        constants.Labels.CONTENT.value] = child.mdwrap.wrapped_data.bin_data

                item = make_item(child_data)
                child_item.appendRow(item)

            amd_item.model.appendRow(child_item)

        metadata.append(amd_item)

    for dmd in dmd_data:
        values = {}
        values[constants.Attributes.ID.value] = get_data(dmd.id)
        values[constants.Attributes.GROUP_ID.value] = get_data(dmd.group_id)
        values[constants.Attributes.ADMID.value] = get_data(dmd.admid)
        values[constants.Attributes.CREATED.value] = get_data(dmd.created)
        values[constants.Attributes.STATUS.value] = get_data(dmd.status)
        values[constants.Labels.TAG.value] = dmd.tag()

        dmd_item = make_item(values)

        if dmd.mdref:
            data = {}
            data[constants.Attributes.ID.value] = get_data(dmd.mdref.id)
            data[constants.Attributes.MIMETYPE.value] = get_data(
                dmd.mdref.mimetype)
            data[constants.Attributes.LABEL.value] = get_data(dmd.mdref.label)
            data[constants.Attributes.LOCTYPE.value] = get_data(
                dmd.mdref.loctype)
            data[constants.Attributes.OTHER_LOCTYPE.value] = get_data(
                dmd.mdref.other_loctype)
            data[constants.Attributes.MD_TYPE.value] = get_data(
                dmd.mdref.mdtype)
            data[constants.Attributes.MD_TYPE_OTHER.value] = get_data(
                dmd.mdref.other_mdtype)
            data[constants.Attributes.MD_TYPE_VERSION.value] = get_data(
                dmd.mdref.mdtype_version)
            data[constants.Attributes.SIZE.value] = get_data(dmd.mdref.size)
            data[constants.Attributes.CREATED.value] = get_data(
                dmd.mdref.created)
            data[constants.Attributes.CHECKSUM.value] = get_data(
                dmd.mdref.checksum)
            data[constants.Attributes.CHECKSUM_TYPE.value] = get_data(
                dmd.mdref.checksum_type)
            data[constants.Attributes.XPTR.value] = get_data(dmd.mdref.xptr)
            data[constants.Attributes.XLINK_ROLE.value] = get_data(
                dmd.mdref.xlink_role)
            data[constants.Attributes.XLINK_ARCROLE.value] = get_data(
                dmd.mdref.xlink_arcrole)
            data[constants.Attributes.XLINK_TITLE.value] = get_data(
                dmd.mdref.xlink_title)
            data[constants.Attributes.XLINK_ACTUATE.value] = get_data(
                dmd.mdref.xlink_actuate)
            data[constants.Attributes.XLINK_HREF.value] = get_data(
                dmd.mdref.xlink_href)
            data[constants.Attributes.XLINK_SHOW.value] = get_data(
                dmd.mdref.xlink_show)
            data[constants.Labels.TAG.value] = dmd.mdref.tag()

            item = make_item(data)
            dmd_item.model.appendRow(item)

        if dmd.mdwrap:
            data = {}
            data[constants.Attributes.ID.value] = get_data(dmd.mdwrap.id)
            data[constants.Attributes.MIMETYPE.value] = get_data(
                dmd.mdwrap.mimetype)
            data[constants.Attributes.LABEL.value] = get_data(dmd.mdwrap.label)
            data[constants.Attributes.MD_TYPE.value] = get_data(
                dmd.mdwrap.mdtype)
            data[constants.Attributes.MD_TYPE_OTHER.value] = get_data(
                dmd.mdwrap.other_mdtype)
            data[constants.Attributes.MD_TYPE_VERSION.value] = get_data(
                dmd.mdwrap.mdtype_version)
            data[constants.Attributes.SIZE.value] = get_data(dmd.mdwrap.size)
            data[constants.Attributes.CREATED.value] = get_data(
                dmd.mdwrap.created)
            data[constants.Attributes.CHECKSUM.value] = get_data(
                dmd.mdwrap.checksum)
            data[constants.Attributes.CHECKSUM_TYPE.value] = get_data(
                dmd.mdwrap.checksum_type)
            data[constants.Labels.TAG.value] = dmd.mdwrap.tag()

            if dmd.mdwrap.wrapped_data.tag() == mets.constants.ElementTags.XML_DATA.value:
                data[
                    constants.Attributes.TYPE.value] = constants.DataContentTypes.XML.value
                data[
                    constants.Labels.CONTENT.value] = dmd.mdwrap.wrapped_data.xml_string()
            else:
                data[
                    constants.Attributes.ID.value] = constants.DataContentTypes.BIN.value
                data[
                    constants.Labels.CONTENT.value] = dmd.mdwrap.wrapped_data.bin_data

            item = make_item(data)
            dmd_item.model.appendRow(item)

        metadata.append(dmd_item)

    return metadata


def metadata_to_xml(data: list[CustomListItem]) -> tuple[
    list[mets.AdministrativeMetadataSection],
    list[mets.DescriptiveMetadataSection]]:
    amd = []
    dmd = []

    for item in data:
        item_data = item.data(Qt.ItemDataRole.UserRole)

        if item_data[
            constants.Labels.TAG.value] == constants.ElementTags.AMD_SEC.value:
            content = []
            for i in range(item.model.rowCount()):
                child = item.model.item(i)
                content.append(transform_metadata(child))

            amd.append(mets.AdministrativeMetadataSection(
                element_id=pass_data(item_data[constants.Attributes.ID.value]),
                content=content,
                other_attribs=None
            ))

        elif item_data[
            constants.Labels.TAG.value] == constants.ElementTags.DMD_SEC.value:
            md_wrap = None
            md_ref = None
            for i in range(item.model.rowCount()):
                child = item.model.item(i)
                item = transform_metadata(child)
                if item.tag() == mets.MetadataReference.tag():
                    md_ref = item

                elif item.tag() == mets.MetadataWrapper.tag():
                    md_wrap = item
            dmd.append(mets.DescriptiveMetadataSection(
                mdwrap=md_wrap,
                mdref=md_ref,
                element_id=pass_data(item_data[constants.Attributes.ID.value]),
                group_id=pass_data(
                    item_data[constants.Attributes.GROUP_ID.value]),
                admid=pass_data(item_data[constants.Attributes.ADMID.value]),
                created=pass_data(
                    item_data[constants.Attributes.CREATED.value]),
                status=pass_data(item_data[constants.Attributes.STATUS.value]),
                other_attribs=None
            ))

    if not amd:
        amd = None
    if not dmd:
        dmd = None

    return amd, dmd


def links_from_xml(data: mets.StructuralLink) -> Union[
    None, tuple[dict, list[QListWidgetItem]]]:
    if not data:
        return None

    values = {constants.Attributes.ID.value: data.id}
    links = []

    for link in data.struct_map_links:
        lnk = {}
        lnk[constants.Attributes.ID.value] = get_data(link.id)
        lnk[constants.Attributes.XLINK_ARCROLE.value] = get_data(
            link.xlink_arcrole)
        lnk[constants.Attributes.XLINK_TITLE.value] = get_data(link.xlink_title)
        lnk[constants.Attributes.XLINK_SHOW.value] = get_data(link.xlink_show)
        lnk[constants.Attributes.XLINK_ACTUATE.value] = get_data(
            link.xlink_actuate)
        lnk[constants.Attributes.XLINK_TO.value] = get_data(link.xlink_to)
        lnk[constants.Attributes.XLINK_FROM.value] = get_data(link.xlink_from)
        lnk[constants.Labels.TAG.value] = link.tag()

        item = make_item(lnk)
        links.append(item)

    for group in data.struct_map_link_groups:
        grp = {}
        grp[constants.Attributes.ID.value] = get_data(group.id)
        grp[constants.Attributes.ARCLINK_ORDER.value] = get_data(
            group.arclink_order)
        grp[constants.Attributes.XLINK_ROLE.value] = get_data(group.xlink_role)
        grp[constants.Attributes.XLINK_TITLE.value] = get_data(
            group.xlink_title)
        grp[constants.Labels.TAG.value] = group.tag()

        group_item = make_item(grp)

        for locator in group.locator_links:
            loc = {}
            loc[constants.Attributes.ID.value] = get_data(locator.id)
            loc[constants.Attributes.XLINK_HREF.value] = get_data(
                locator.xlink_href)
            loc[constants.Attributes.XLINK_LABEL.value] = get_data(
                locator.xlink_label)
            loc[constants.Attributes.XLINK_ROLE.value] = get_data(
                locator.xlink_role)
            loc[constants.Attributes.XLINK_TITLE.value] = get_data(
                locator.xlink_title)
            loc[constants.Labels.TAG.value] = locator.tag()

            item = make_item(loc)
            group_item.appendRow(item)

        for arc_link in group.arclinks:
            arc = {}
            arc[constants.Attributes.ID.value] = get_data(arc_link.id)
            arc[constants.Attributes.ARC_TYPE.value] = get_data(
                arc_link.arctype)
            arc[constants.Attributes.ADMID.value] = get_data(arc_link.admid)
            arc[constants.Attributes.XLINK_ACTUATE.value] = get_data(
                arc_link.xlink_actuate)
            arc[constants.Attributes.XLINK_ARCROLE.value] = get_data(
                arc_link.xlink_arcrole)
            arc[constants.Attributes.XLINK_FROM.value] = get_data(
                arc_link.xlink_from)
            arc[constants.Attributes.XLINK_SHOW.value] = get_data(
                arc_link.xlink_show)
            arc[constants.Attributes.XLINK_TITLE.value] = get_data(
                arc_link.xlink_title)
            arc[constants.Attributes.XLINK_TO.value] = get_data(
                arc_link.xlink_to)
            arc[constants.Labels.TAG.value] = arc_link.tag()

            item = make_item(arc)
            group_item.appendRow(item)

        links.append(group_item)
    return values, links


def links_to_xml(
        data: tuple[dict, list[QStandardItem]]) -> mets.StructuralLink:
    values = data[0]
    links = data[1]

    link_section = None

    link_elements = []
    group_elements = []
    for link in links:
        data = link.data(Qt.ItemDataRole.UserRole)
        if data[
            constants.Labels.TAG.value] == constants.ElementTags.STRUCT_LINK.value:
            link_elements.append(
                mets.StructuralMapLink(xlink_from=pass_data(
                    data[constants.Attributes.XLINK_FROM.value]),
                    xlink_to=pass_data(data[
                                           constants.Attributes.XLINK_TO.value]),
                    element_id=pass_data(data[
                                             constants.Attributes.ID.value]),
                    xlink_arcrole=pass_data(data[
                                                constants.Attributes.XLINK_ARCROLE.value]),
                    xlink_actuate=pass_data(data[
                                                constants.Attributes.XLINK_ACTUATE.value]),
                    xlink_title=pass_data(data[
                                              constants.Attributes.XLINK_TITLE.value]),
                    xlink_show=pass_data(data[
                                             constants.Attributes.XLINK_SHOW.value])
                ))

        elif data[
            constants.Labels.TAG.value] == constants.ElementTags.STRUCT_LINK_GROUP.value:
            locator_links = []
            arc_links = []
            for i in range(link.rowCount()):
                child_data = link.child(i).data(Qt.ItemDataRole.UserRole)
                if child_data[
                    constants.Labels.TAG.value] == constants.ElementTags.LOCATOR_LINK.value:
                    locator_links.append(
                        mets.StructuralMapLocatorLink(
                            xlink_href=pass_data(child_data[
                                                     constants.Attributes.XLINK_HREF.value]),
                            element_id=pass_data(
                                child_data[constants.Attributes.ID.value]),
                            xlink_label=pass_data(child_data[
                                                      constants.Attributes.XLINK_LABEL.value]),
                            xlink_role=pass_data(child_data[
                                                     constants.Attributes.XLINK_ROLE.value]),
                            xlink_title=pass_data(child_data[
                                                      constants.Attributes.XLINK_TITLE.value])
                        )
                    )

                elif child_data[
                    constants.Labels.TAG.value] == constants.ElementTags.ARC_LINK.value:
                    arc_links.append(
                        mets.StructuralMapArcLink(
                            element_id=pass_data(
                                child_data[constants.Attributes.ID.value]),
                            admid=pass_data(
                                child_data[constants.Attributes.ADMID.value]),
                            arctype=pass_data(child_data[
                                                  constants.Attributes.ARC_TYPE.value]),
                            xlink_arcrole=pass_data(child_data[
                                                        constants.Attributes.XLINK_ARCROLE.value]),
                            xlink_title=pass_data(child_data[
                                                      constants.Attributes.XLINK_TITLE.value]),
                            xlink_from=pass_data(child_data[
                                                     constants.Attributes.XLINK_FROM.value]),
                            xlink_to=pass_data(child_data[
                                                   constants.Attributes.XLINK_TO.value]),
                            xlink_show=pass_data(child_data[
                                                     constants.Attributes.XLINK_SHOW.value]),
                            xlink_actuate=pass_data(child_data[
                                                        constants.Attributes.XLINK_ACTUATE.value])
                        )
                    )

            group_elements.append(
                mets.StructuralMapLinkGroup(locator_links=locator_links,
                                            arclinks=arc_links,
                                            element_id=pass_data(data[
                                                                     constants.Attributes.ID.value]),
                                            arclink_order=pass_data(data[
                                                                        constants.Attributes.ARCLINK_ORDER.value]),
                                            xlink_role=pass_data(data[
                                                                     constants.Attributes.XLINK_ROLE.value]),
                                            xlink_title=pass_data(data[
                                                                      constants.Attributes.XLINK_TITLE.value]))
            )
    if link_elements or group_elements:
        link_section = mets.StructuralLink(
            element_id=pass_data(values[constants.Attributes.ID.value]),
            struct_map_links=link_elements,
            struct_map_link_groups=group_elements,
            other_attribs=None)

    return link_section


def behaviour_from_xml(data: list[mets.BehaviorSection]) -> list[
    QStandardItem]:
    behaviour_section_elements = []
    for item in data:
        element = process_behaviour_elements(item)
        behaviour_section_elements.append(element)
    return behaviour_section_elements


def behaviour_to_xml(data: list[QStandardItem]) -> list[
    mets.BehaviorSection]:
    behaviour_section_elements = []
    for item in data:
        element = transform_behaviour_element(item)
        behaviour_section_elements.append(element)
    return behaviour_section_elements


def mets_from_xml(data: mets.METSDocument) -> tuple[dict, list, list]:
    values = {}
    values[constants.Attributes.ID.value] = get_data(data.id)
    values[constants.Attributes.OBJID.value] = get_data(data.objid)
    values[constants.Attributes.LABEL.value] = get_data(data.label)
    values[constants.Attributes.TYPE.value] = get_data(data.type)
    values[constants.Attributes.PROFILE.value] = get_data(data.profile)

    namespaces = []
    for namespace in data._namespaces:
        nms = {}
        nms[constants.Attributes.NAME.value] = namespace
        nms[constants.Labels.VALUE.value] = data._namespaces[namespace]
        nms[constants.Labels.TAG.value] = constants.Labels.NAMESPACES.value
        namespaces.append(nms)

    other_attribs = []
    for attrib in data.other_attribs:
        attr = {}
        attr[constants.Attributes.NAME.value] = attrib
        attr[constants.Labels.VALUE.value] = data.other_attribs[attrib]
        attr[constants.Labels.TAG.value] = constants.Labels.OTHER_ATTRIBS.value
        other_attribs.append(attr)

    return values, namespaces, other_attribs


def mets_to_xml(data,
                structure_sec: list[mets.StructuralMap],
                file_sec: mets.FileSection,
                header: mets.Header,
                amd: list[mets.AdministrativeMetadataSection],
                dmd: list[mets.DescriptiveMetadataSection],
                link_sec: mets.StructuralLink,
                behaviour_sec: list[
                    mets.BehaviorSection]) -> mets.METSDocument:
    values = data[0]
    namespaces = data[1]  # TODO: namespace addition
    other_attribs = transform_other_attribs(
        values[constants.Labels.OTHER_ATTRIBS.value])

    return mets.METSDocument(struct_map=structure_sec,
                             header=header,
                             amd=amd,
                             dmd=dmd,
                             file_sec=file_sec,
                             struct_link=link_sec,
                             behavior=behaviour_sec,
                             element_id=pass_data(
                                 values[constants.Attributes.ID.value]),
                             objid=pass_data(
                                 values[constants.Attributes.OBJID.value]),
                             label=pass_data(
                                 values[constants.Attributes.LABEL.value]),
                             mets_type=pass_data(
                                 values[constants.Attributes.TYPE.value]),
                             profile=pass_data(values[
                                                   constants.Attributes.PROFILE.value]),
                             other_attribs=other_attribs)


# ----------------------------------------------------------------------


# helper function for transforming data from educelab.mets to
# gui internal string-based format
def get_data(field: Any) -> str:
    if field is None:
        return ''
    else:
        return str(field)


# reverse of the get_data function - passing string-based internal
# format to educelab.mets format
def pass_data(field: Any) -> Union[str, None]:
    if field:
        return field
    else:
        return None


# helper functions for transforming individual mets elements between
# educelab.mets and gui
# ----------------------------------------------------------------------
def process_struct_map(struct_item: Union[
    mets.Division, mets.FilePointer, mets.METSPointer, mets.Area,
    mets.SequenceOfFiles, mets.ParallelFiles]) -> QStandardItem:
    item = None
    values = {}
    if struct_item.tag() == constants.ElementTags.DIV.value:
        values[constants.Attributes.ID.value] = get_data(struct_item.id)
        values[constants.Attributes.TYPE.value] = get_data(struct_item.type)
        values[constants.Attributes.LABEL.value] = get_data(struct_item.label)
        values[constants.Attributes.ADMID.value] = get_data(struct_item.admid)
        values[constants.Attributes.CONTENT_IDS.value] = get_data(
            struct_item.content_ids)
        values[constants.Attributes.DMDID.value] = get_data(struct_item.dmdid)
        values[constants.Attributes.ORDER.value] = get_data(struct_item.order)
        values[constants.Attributes.ORDER_LABEL.value] = get_data(
            struct_item.order_label)
        values[constants.Attributes.XLINK_LABEL.value] = get_data(
            struct_item.xlink_label)
        values[constants.Labels.TAG.value] = constants.ElementTags.DIV.value

        item = make_item(values)
        if struct_item.content:
            for content_item in struct_item.content:
                item.appendRow(process_struct_map(content_item))

    elif struct_item.tag() == constants.ElementTags.FPTR.value:
        values[constants.Attributes.ID.value] = get_data(struct_item.id)
        values[constants.Attributes.FILE_ID.value] = get_data(
            struct_item.file_id)
        values[constants.Attributes.CONTENT_IDS.value] = get_data(
            struct_item.content_ids)
        values[constants.Labels.TAG.value] = constants.ElementTags.FPTR.value

        item = make_item(values)
        if struct_item.content:
            item.model().appendRow(process_struct_map(struct_item.content))

    elif struct_item.tag() == constants.ElementTags.MPTR.value:
        values[constants.Attributes.ID.value] = get_data(struct_item.id)
        values[constants.Attributes.CONTENT_IDS.value] = get_data(
            struct_item.content_ids)
        values[constants.Attributes.LOCTYPE.value] = get_data(
            struct_item.loctype)
        values[constants.Attributes.OTHER_LOCTYPE.value] = get_data(
            struct_item.other_loctype)
        values[constants.Attributes.XLINK_ROLE.value] = get_data(
            struct_item.xlink_role)
        values[constants.Attributes.XLINK_ARCROLE.value] = get_data(
            struct_item.xlink_arcrole)
        values[constants.Attributes.XLINK_TITLE.value] = get_data(
            struct_item.xlink_title)
        values[constants.Attributes.XLINK_ACTUATE.value] = get_data(
            struct_item.xlink_actuate)
        values[constants.Attributes.XLINK_HREF.value] = get_data(
            struct_item.xlink_href)
        values[constants.Attributes.XLINK_SHOW.value] = get_data(
            struct_item.xlink_show)
        values[constants.Labels.TAG.value] = constants.ElementTags.MPTR.value

        item = make_item(values)

    elif struct_item.tag() == constants.ElementTags.AREA.value:
        values[constants.Attributes.ID.value] = get_data(struct_item.id)
        values[constants.Attributes.CONTENT_IDS.value] = get_data(
            struct_item.content_ids)
        values[constants.Attributes.ADMID.value] = get_data(struct_item.admid)
        values[constants.Attributes.LABEL.value] = get_data(struct_item.label)
        values[constants.Attributes.ORDER.value] = get_data(struct_item.order)
        values[constants.Attributes.ORDER_LABEL.value] = get_data(
            struct_item.order_label)
        values[constants.Attributes.BEGIN.value] = get_data(struct_item.begin)
        values[constants.Attributes.BETYPE.value] = get_data(struct_item.betype)
        values[constants.Attributes.COORDS.value] = get_data(struct_item.coords)
        values[constants.Attributes.END.value] = get_data(struct_item.end)
        values[constants.Attributes.EXTEND.value] = get_data(struct_item.extent)
        values[constants.Attributes.EXT_TYPE.value] = get_data(
            struct_item.extent_type)
        values[constants.Attributes.FILE_ID.value] = get_data(
            struct_item.file_id)
        values[constants.Attributes.SHAPE.value] = get_data(struct_item.shape)
        values[constants.Labels.TAG.value] = constants.ElementTags.AREA.value

        item = make_item(values)

    elif struct_item.tag() == constants.ElementTags.SEQ.value:
        values[constants.Attributes.ID.value] = get_data(struct_item.id)
        values[constants.Attributes.LABEL.value] = get_data(struct_item.label)
        values[constants.Attributes.ORDER.value] = get_data(struct_item.order)
        values[constants.Attributes.ORDER_LABEL.value] = get_data(
            struct_item.order_label)
        values[constants.Labels.TAG.value] = constants.ElementTags.SEQ.value
        item = make_item(values)
        if struct_item.content:
            for content_item in struct_item.content:
                item.model().appendRow(process_struct_map(content_item))

    elif struct_item.tag() == constants.ElementTags.PAR.value:
        values[constants.Attributes.ID.value] = get_data(struct_item.id)
        values[constants.Attributes.LABEL.value] = get_data(struct_item.label)
        values[constants.Attributes.ORDER.value] = get_data(struct_item.order)
        values[constants.Attributes.ORDER_LABEL.value] = get_data(
            struct_item.order_label)
        values[constants.Labels.TAG.value] = constants.ElementTags.PAR.value
        item = make_item(values)
        if struct_item.content:
            for content_item in struct_item.content:
                item.model().appendRow(process_struct_map(content_item))

    else:
        print(struct_item.tag())

    return item


def process_file_elements(file_element) -> QStandardItem:
    item = None
    values = {}

    if file_element.tag() == constants.ElementTags.FILE_GROUP.value:
        values[constants.Attributes.ID.value] = get_data(file_element.id)
        values[constants.Attributes.ADMID.value] = get_data(file_element.admid)
        values[constants.Attributes.USE.value] = get_data(file_element.use)
        values[constants.Attributes.VERSDATE.value] = get_data(
            file_element.versdate)
        values[
            constants.Labels.TAG.value] = constants.ElementTags.FILE_GROUP.value

        item = make_item(values)
        if file_element.content:
            for content_item in file_element.content:
                item.appendRow(process_file_elements(content_item))

    elif file_element.tag() == constants.ElementTags.FILE.value:
        values[constants.Attributes.ID.value] = get_data(file_element.id)
        values[constants.Attributes.ADMID.value] = get_data(file_element.admid)
        values[constants.Attributes.USE.value] = get_data(file_element.use)
        values[constants.Attributes.DMDID.value] = get_data(file_element.dmdid)
        values[constants.Attributes.BEGIN.value] = get_data(file_element.begin)
        values[constants.Attributes.BETYPE.value] = get_data(
            file_element.betype)
        values[constants.Attributes.CHECKSUM.value] = get_data(
            file_element.checksum)
        values[constants.Attributes.CHECKSUM_TYPE.value] = get_data(
            file_element.checksum_type)
        values[constants.Attributes.CREATED.value] = get_data(
            file_element.created)
        values[constants.Attributes.END.value] = get_data(file_element.end)
        values[constants.Attributes.GROUP_ID.value] = get_data(
            file_element.group_id)
        values[constants.Attributes.MIMETYPE.value] = get_data(
            file_element.mimetype)
        values[constants.Attributes.OWNER_ID.value] = get_data(
            file_element.owner_id)
        values[constants.Attributes.SEQ.value] = get_data(file_element.sequence)
        values[constants.Attributes.SIZE.value] = get_data(file_element.size)
        values[constants.Labels.TAG.value] = constants.ElementTags.FILE.value

        item = make_item(values)
        if file_element.content:
            for content_item in file_element.content:
                item.appendRow(process_file_elements(content_item))

    elif file_element.tag() == constants.ElementTags.FILE_LOCATION.value:
        values[constants.Attributes.ID.value] = get_data(file_element.id)
        values[constants.Attributes.LOCTYPE.value] = get_data(
            file_element.loctype)
        values[constants.Attributes.OTHER_LOCTYPE.value] = get_data(
            file_element.other_loctype)
        values[constants.Attributes.USE.value] = get_data(file_element.use)
        values[constants.Attributes.XLINK_ROLE.value] = get_data(
            file_element.xlink_role)
        values[constants.Attributes.XLINK_ARCROLE.value] = get_data(
            file_element.xlink_arcrole)
        values[constants.Attributes.XLINK_TITLE.value] = get_data(
            file_element.xlink_title)
        values[constants.Attributes.XLINK_ACTUATE.value] = get_data(
            file_element.xlink_actuate)
        values[constants.Attributes.XLINK_HREF.value] = get_data(
            file_element.xlink_href)
        values[constants.Attributes.XLINK_SHOW.value] = get_data(
            file_element.xlink_show)
        values[
            constants.Labels.TAG.value] = constants.ElementTags.FILE_LOCATION.value

        item = make_item(values)

    elif file_element.tag() == constants.ElementTags.FILE_CONTENT.value:
        values[constants.Attributes.ID.value] = get_data(file_element.id)
        values[constants.Attributes.USE.value] = get_data(file_element.use)
        values[
            constants.Labels.TAG.value] = constants.ElementTags.FILE_CONTENT.value
        if file_element.content.tag() == mets.ElementTags.XML_DATA:
            values[
                constants.Attributes.TYPE.value] = constants.DataContentTypes.XML.value
            values[
                constants.Labels.CONTENT.value] = file_element.content.xml_data
        elif file_element.content.tag() == mets.ElementTags.BIN_DATA:
            values[
                constants.Attributes.TYPE.value] = constants.DataContentTypes.BIN.value
            values[
                constants.Labels.CONTENT.value] = file_element.content.bin_data

        item = make_item(values)

    elif file_element.tag() == constants.ElementTags.STREAM.value:
        values[constants.Attributes.ID.value] = get_data(file_element.id)
        values[constants.Attributes.ADMID.value] = get_data(file_element.admid)
        values[constants.Attributes.BEGIN.value] = get_data(file_element.begin)
        values[constants.Attributes.BETYPE.value] = get_data(
            file_element.betype)
        values[constants.Attributes.END.value] = get_data(file_element.end)
        values[constants.Attributes.DMDID.value] = get_data(file_element.dmdid)
        values[constants.Attributes.OWNER_ID.value] = get_data(
            file_element.owner_id)
        values[constants.Attributes.STREAM_TYPE.value] = get_data(
            file_element.stream_type)

        values[constants.Labels.TAG.value] = constants.ElementTags.STREAM.value

        item = make_item(values)

    elif file_element.tag() == constants.ElementTags.TRANSFORM_FILE.value:
        values[constants.Attributes.ID.value] = get_data(file_element.id)
        values[constants.Attributes.TRANSFORM_ALGORITHM.value] = get_data(
            file_element.algorithm)
        values[constants.Attributes.TRANSFORM_BEHAVIOR.value] = get_data(
            file_element.behavior)
        values[constants.Attributes.TRANSFORM_KEY.value] = get_data(
            file_element.key)
        values[constants.Attributes.TRANSFORM_ORDER.value] = get_data(
            file_element.order)
        values[constants.Attributes.TRANSFORM_TYPE.value] = get_data(
            file_element.transform_type)
        values[
            constants.Labels.TAG.value] = constants.ElementTags.TRANSFORM_FILE.value

        item = make_item(values)

    return item


def process_behaviour_elements(behaviour_element) -> QStandardItem:
    item = None
    values = {}

    if behaviour_element.tag() == constants.ElementTags.BEHAVIOUR_SEC.value:
        values[constants.Attributes.ID.value] = get_data(behaviour_element.id)
        values[constants.Attributes.CREATED.value] = get_data(
            behaviour_element.created)
        values[constants.Attributes.LABEL.value] = get_data(
            behaviour_element.label)
        values[
            constants.Labels.TAG.value] = constants.ElementTags.BEHAVIOUR_SEC.value

        values[constants.Labels.OTHER_ATTRIBS.value] = process_other_attribs(
            behaviour_element.other_attribs)

        item = make_item(values)
        if behaviour_element.content:
            for content_item in behaviour_element.content:
                item.appendRow(process_behaviour_elements(content_item))

    elif behaviour_element.tag() == constants.ElementTags.BEHAVIOUR.value:
        values[constants.Attributes.ID.value] = get_data(behaviour_element.id)
        values[constants.Attributes.ADMID.value] = get_data(
            behaviour_element.admid)
        values[constants.Attributes.LABEL.value] = get_data(
            behaviour_element.label)
        values[constants.Attributes.STRUCTID.value] = get_data(
            behaviour_element.struct_id)
        values[constants.Attributes.CREATED.value] = get_data(
            behaviour_element.created)
        values[constants.Attributes.BTYPE.value] = get_data(
            behaviour_element.btype)
        values[constants.Attributes.GROUP_ID.value] = get_data(
            behaviour_element.group_id)
        values[
            constants.Labels.TAG.value] = constants.ElementTags.BEHAVIOUR.value

        item = make_item(values)
        item.appendRow(process_behaviour_elements(behaviour_element.mechanism))

        if behaviour_element.interface_def:
            item.appendRow(
                process_behaviour_elements(behaviour_element.interface_def))

    elif behaviour_element.tag() == constants.ElementTags.MECHANISM.value:
        values[constants.Attributes.ID.value] = get_data(behaviour_element.id)
        values[constants.Attributes.LOCTYPE.value] = get_data(
            behaviour_element.loctype)
        values[constants.Attributes.LABEL.value] = get_data(
            behaviour_element.label)
        values[constants.Attributes.OTHER_LOCTYPE.value] = get_data(
            behaviour_element.other_loctype)
        values[constants.Attributes.XLINK_ROLE.value] = get_data(
            behaviour_element.xlink_role)
        values[constants.Attributes.XLINK_ARCROLE.value] = get_data(
            behaviour_element.xlink_arcrole)
        values[constants.Attributes.XLINK_TITLE.value] = get_data(
            behaviour_element.xlink_title)
        values[constants.Attributes.XLINK_ACTUATE.value] = get_data(
            behaviour_element.xlink_actuate)
        values[constants.Attributes.XLINK_HREF.value] = get_data(
            behaviour_element.xlink_href)
        values[constants.Attributes.XLINK_SHOW.value] = get_data(
            behaviour_element.xlink_show)
        values[
            constants.Labels.TAG.value] = constants.ElementTags.MECHANISM.value

        item = make_item(values)

    elif behaviour_element.tag() == constants.ElementTags.INTERFACE_DEFINITION.value:
        values[constants.Attributes.ID.value] = get_data(behaviour_element.id)
        values[constants.Attributes.LOCTYPE.value] = get_data(
            behaviour_element.loctype)
        values[constants.Attributes.LABEL.value] = get_data(
            behaviour_element.label)
        values[constants.Attributes.OTHER_LOCTYPE.value] = get_data(
            behaviour_element.other_loctype)
        values[constants.Attributes.XLINK_ROLE.value] = get_data(
            behaviour_element.xlink_role)
        values[constants.Attributes.XLINK_ARCROLE.value] = get_data(
            behaviour_element.xlink_arcrole)
        values[constants.Attributes.XLINK_TITLE.value] = get_data(
            behaviour_element.xlink_title)
        values[constants.Attributes.XLINK_ACTUATE.value] = get_data(
            behaviour_element.xlink_actuate)
        values[constants.Attributes.XLINK_HREF.value] = get_data(
            behaviour_element.xlink_href)
        values[constants.Attributes.XLINK_SHOW.value] = get_data(
            behaviour_element.xlink_show)
        values[
            constants.Labels.TAG.value] = constants.ElementTags.INTERFACE_DEFINITION.value

        item = make_item(values)

    return item


def process_other_attribs(element_attribs: dict[str, str]) -> list[dict]:
    other_attribs = []
    for attrib in element_attribs:
        attr = {}
        attr[constants.Attributes.NAME.value] = attrib
        attr[constants.Labels.VALUE.value] = element_attribs[attrib]
        attr[constants.Labels.TAG.value] = constants.Labels.OTHER_ATTRIBS.value
        other_attribs.append(attr)
    return other_attribs


def transform_metadata(item: QStandardItem):
    item_data = item.data(Qt.ItemDataRole.UserRole)
    result = None

    if item_data[
        constants.Labels.TAG.value] == constants.ElementTags.MD_WRAP.value:
        content = None
        if item_data[
            constants.Attributes.TYPE.value] == constants.DataContentTypes.XML.value:
            content = mets.XMLData(
                item_data[constants.Labels.CONTENT.value])
        elif item_data[
            constants.Attributes.TYPE.value] == constants.DataContentTypes.BIN.value:
            content = mets.BinData(
                item_data[constants.Labels.CONTENT.value])
        result = mets.MetadataWrapper(
            mdtype=pass_data(item_data[constants.Attributes.MD_TYPE.value]),
            wrapped_data=content,
            element_id=pass_data(item_data[constants.Attributes.ID.value]),
            mimetype=pass_data(item_data[constants.Attributes.MIMETYPE.value]),
            label=pass_data(item_data[constants.Attributes.LABEL.value]),
            mdtype_version=pass_data(
                item_data[constants.Attributes.MD_TYPE_VERSION.value]),
            other_mdtype=pass_data(
                item_data[constants.Attributes.MD_TYPE_OTHER.value]),
            size=pass_data(item_data[constants.Attributes.SIZE.value]),
            created=pass_data(item_data[constants.Attributes.CREATED.value]),
            checksum=pass_data(item_data[constants.Attributes.CHECKSUM.value]),
            checksum_type=pass_data(
                item_data[constants.Attributes.CHECKSUM_TYPE.value])
        )

    elif item_data[
        constants.Labels.TAG.value] == constants.ElementTags.MD_REF.value:
        result = mets.MetadataReference(
            loctype=pass_data(item_data[constants.Attributes.LOCTYPE.value]),
            mdtype=pass_data(item_data[constants.Attributes.MD_TYPE.value]),
            xlink_href=pass_data(
                item_data[constants.Attributes.XLINK_HREF.value]),
            xptr=pass_data(item_data[constants.Attributes.XPTR.value]),
            other_loctype=pass_data(
                item_data[constants.Attributes.OTHER_LOCTYPE.value]),
            element_id=pass_data(item_data[constants.Attributes.ID.value]),
            mimetype=pass_data(item_data[constants.Attributes.MIMETYPE.value]),
            label=pass_data(item_data[constants.Attributes.LABEL.value]),
            mdtype_version=pass_data(
                item_data[constants.Attributes.MD_TYPE_VERSION.value]),
            other_mdtype=pass_data(
                item_data[constants.Attributes.MD_TYPE_OTHER.value]),
            size=pass_data(item_data[constants.Attributes.SIZE.value]),
            created=pass_data(item_data[constants.Attributes.CREATED.value]),
            checksum=pass_data(item_data[constants.Attributes.CHECKSUM.value]),
            checksum_type=pass_data(
                item_data[constants.Attributes.CHECKSUM_TYPE.value]),
            xlink_role=pass_data(
                item_data[constants.Attributes.XLINK_ROLE.value]),
            xlink_arcrole=pass_data(
                item_data[constants.Attributes.XLINK_ARCROLE.value]),
            xlink_actuate=pass_data(
                item_data[constants.Attributes.XLINK_ACTUATE.value]),
            xlink_title=pass_data(
                item_data[constants.Attributes.XLINK_TITLE.value]),
            xlink_show=pass_data(
                item_data[constants.Attributes.XLINK_SHOW.value])
        )

    else:
        md_ref = None
        md_wrap = None

        for i in range(item.rowCount()):
            child = transform_metadata(item.child(i))
            if child.tag() == mets.MetadataReference.tag():
                md_ref = child

            elif child.tag() == mets.MetadataWrapper.tag():
                md_wrap = child

        if item_data[
            constants.Labels.TAG.value] == constants.ElementTags.TECH_MD.value:
            result = mets.TechnicalMetadata(
                element_id=pass_data(item_data[constants.Attributes.ID.value]),
                group_id=pass_data(
                    item_data[constants.Attributes.GROUP_ID.value]),
                admid=pass_data(item_data[constants.Attributes.ADMID.value]),
                created=pass_data(
                    item_data[constants.Attributes.CREATED.value]),
                status=pass_data(item_data[constants.Attributes.STATUS.value]),
                mdwrap=md_wrap,
                mdref=md_ref)

        elif item_data[
            constants.Labels.TAG.value] == constants.ElementTags.SOURCE_MD.value:
            result = mets.SourceMetadata(
                element_id=pass_data(item_data[constants.Attributes.ID.value]),
                group_id=pass_data(
                    item_data[constants.Attributes.GROUP_ID.value]),
                admid=pass_data(item_data[constants.Attributes.ADMID.value]),
                created=pass_data(
                    item_data[constants.Attributes.CREATED.value]),
                status=pass_data(item_data[constants.Attributes.STATUS.value]),
                mdwrap=md_wrap,
                mdref=md_ref)

        elif item_data[
            constants.Labels.TAG.value] == constants.ElementTags.RIGHTS_MD.value:
            result = mets.PropertyRightsMetadata(
                element_id=pass_data(item_data[constants.Attributes.ID.value]),
                group_id=pass_data(
                    item_data[constants.Attributes.GROUP_ID.value]),
                admid=pass_data(item_data[constants.Attributes.ADMID.value]),
                created=pass_data(
                    item_data[constants.Attributes.CREATED.value]),
                status=pass_data(item_data[constants.Attributes.STATUS.value]),
                mdwrap=md_wrap,
                mdref=md_ref)

        elif item_data[
            constants.Labels.TAG.value] == constants.ElementTags.DIGIPROV_MD.value:
            result = mets.DigitalProvenanceMetadata(
                element_id=pass_data(item_data[constants.Attributes.ID.value]),
                group_id=pass_data(
                    item_data[constants.Attributes.GROUP_ID.value]),
                admid=pass_data(item_data[constants.Attributes.ADMID.value]),
                created=pass_data(
                    item_data[constants.Attributes.CREATED.value]),
                status=pass_data(item_data[constants.Attributes.STATUS.value]),
                mdwrap=md_wrap,
                mdref=md_ref)

    return result


def transform_struct_map(item: QStandardItem) -> Union[
    mets.Division, mets.METSPointer, mets.FilePointer,
    mets.SequenceOfFiles, mets.Area, mets.ParallelFiles]:
    result = None
    item_data = item.data(Qt.ItemDataRole.UserRole)
    if item_data[constants.Labels.TAG.value] == constants.ElementTags.DIV.value:
        content = []
        for i in range(item.rowCount()):
            content.append(transform_struct_map(item.child(i)))
        result = mets.Division(content=content,
                               element_id=pass_data(item_data[
                                                        constants.Attributes.ID.value]),
                               order=pass_data(item_data[
                                                   constants.Attributes.ORDER.value]),
                               order_label=pass_data(item_data[
                                                         constants.Attributes.ORDER_LABEL.value]),
                               label=pass_data(item_data[
                                                   constants.Attributes.LABEL.value]),
                               admid=pass_data(item_data[
                                                   constants.Attributes.ADMID.value]),
                               dmdid=pass_data(item_data[
                                                   constants.Attributes.DMDID.value]),
                               div_type=pass_data(item_data[
                                                      constants.Attributes.TYPE.value]),
                               content_ids=pass_data(item_data[
                                                         constants.Attributes.CONTENT_IDS.value]),
                               xlink_label=pass_data(item_data[
                                                         constants.Attributes.XLINK_LABEL.value]))

    elif item_data[
        constants.Labels.TAG.value] == constants.ElementTags.MPTR.value:
        result = mets.METSPointer(
            loctype=pass_data(item_data[constants.Attributes.LOCTYPE.value]),
            element_id=pass_data(item_data[constants.Attributes.ID.value]),
            other_loctype=pass_data(
                item_data[constants.Attributes.OTHER_LOCTYPE.value]),
            content_ids=pass_data(
                item_data[constants.Attributes.CONTENT_IDS.value]),
            xlink_actuate=pass_data(
                item_data[constants.Attributes.XLINK_ACTUATE.value]),
            xlink_arcrole=pass_data(
                item_data[constants.Attributes.XLINK_ARCROLE.value]),
            xlink_show=pass_data(
                item_data[constants.Attributes.XLINK_SHOW.value]),
            xlink_title=pass_data(
                item_data[constants.Attributes.XLINK_TITLE.value]),
            xlink_role=pass_data(
                item_data[constants.Attributes.XLINK_ROLE.value]),
            xlink_href=pass_data(
                item_data[constants.Attributes.XLINK_HREF.value])
        )

    elif item_data[
        constants.Labels.TAG.value] == constants.ElementTags.FPTR.value:
        content = None
        for i in range(item.rowCount()):
            content = transform_struct_map(item.child(i))

        result = mets.FilePointer(
            content=content,
            element_id=pass_data(item_data[constants.Attributes.ID.value]),
            file_id=pass_data(item_data[constants.Attributes.FILE_ID.value]),
            content_ids=pass_data(
                item_data[constants.Attributes.CONTENT_IDS.value]),
            other_attribs=None
        )

    elif item_data[
        constants.Labels.TAG.value] == constants.ElementTags.SEQ.value:
        content = []
        for i in range(item.rowCount()):
            content.append(transform_struct_map(item.child(i)))

        result = mets.SequenceOfFiles(
            content=content,
            element_id=pass_data(item_data[constants.Attributes.ID.value]),
            label=pass_data(item_data[constants.Attributes.LABEL.value]),
            order=pass_data(item_data[constants.Attributes.ORDER.value]),
            order_label=pass_data(
                item_data[constants.Attributes.ORDER_LABEL.value]),
            other_attribs=None
        )

    elif item_data[
        constants.Labels.TAG.value] == constants.ElementTags.AREA.value:
        result = mets.Area(
            file_id=pass_data(item_data[constants.Attributes.FILE_ID.value]),
            element_id=pass_data(item_data[constants.Attributes.ID.value]),
            shape=pass_data(item_data[constants.Attributes.SHAPE.value]),
            coords=pass_data(item_data[constants.Attributes.COORDS.value]),
            begin=pass_data(item_data[constants.Attributes.BEGIN.value]),
            end=pass_data(item_data[constants.Attributes.END.value]),
            betype=pass_data(item_data[constants.Attributes.BETYPE.value]),
            extent=pass_data(item_data[constants.Attributes.EXTEND.value]),
            extent_type=pass_data(
                item_data[constants.Attributes.EXT_TYPE.value]),
            admid=pass_data(item_data[constants.Attributes.ADMID.value]),
            content_ids=pass_data(
                item_data[constants.Attributes.CONTENT_IDS.value]),
            label=pass_data(item_data[constants.Attributes.LABEL.value]),
            order=pass_data(item_data[constants.Attributes.ORDER.value]),
            order_label=pass_data(
                item_data[constants.Attributes.ORDER_LABEL.value]),
            other_attribs=None
        )

    elif item_data[
        constants.Labels.TAG.value] == constants.ElementTags.PAR.value:
        content = []
        for i in range(item.rowCount()):
            content.append(transform_struct_map(item.child(i)))

        result = mets.ParallelFiles(
            content=content,
            element_id=pass_data(item_data[constants.Attributes.ID.value]),
            label=pass_data(item_data[constants.Attributes.LABEL.value]),
            order=pass_data(item_data[constants.Attributes.ORDER.value]),
            order_label=pass_data(
                item_data[constants.Attributes.ORDER_LABEL.value]),
            other_attribs=None
        )

    return result


def transform_file_element(item: QStandardItem) -> Union[
    mets.FileGroup, mets.File, mets.FileLocation,
    mets.FileContent, mets.Stream, mets.TransformFile]:
    element = None
    item_data = item.data(Qt.ItemDataRole.UserRole)

    if item_data[
        constants.Labels.TAG.value] == constants.ElementTags.FILE_GROUP.value:
        content = []
        for i in range(item.rowCount()):
            content.append(transform_file_element(item.child(i)))

        element = mets.FileGroup(content=content,
                                 element_id=pass_data(item_data[
                                                          constants.Attributes.ID.value]),
                                 versdate=pass_data(item_data[
                                                        constants.Attributes.VERSDATE.value]),
                                 admid=pass_data(item_data[
                                                     constants.Attributes.ADMID.value]),
                                 use=pass_data(item_data[
                                                   constants.Attributes.USE.value]),
                                 other_attribs=None)

    elif item_data[
        constants.Labels.TAG.value] == constants.ElementTags.FILE.value:
        content = []
        for i in range(item.rowCount()):
            content.append(transform_file_element(item.child(i)))

        element = mets.File(
            element_id=pass_data(item_data[constants.Attributes.ID.value]),
            content=content,
            sequence=pass_data(item_data[constants.Attributes.SEQ.value]),
            mimetype=pass_data(item_data[constants.Attributes.MIMETYPE.value]),
            size=pass_data(item_data[constants.Attributes.SIZE.value]),
            created=pass_data(item_data[constants.Attributes.CREATED.value]),
            checksum=pass_data(item_data[constants.Attributes.CHECKSUM.value]),
            checksum_type=pass_data(
                item_data[constants.Attributes.CHECKSUM_TYPE.value]),
            owner_id=pass_data(item_data[constants.Attributes.OWNER_ID.value]),
            admid=pass_data(item_data[constants.Attributes.ADMID.value]),
            dmdid=pass_data(item_data[constants.Attributes.DMDID.value]),
            group_id=pass_data(item_data[constants.Attributes.GROUP_ID.value]),
            use=pass_data(item_data[constants.Attributes.USE.value]),
            begin=pass_data(item_data[constants.Attributes.BEGIN.value]),
            end=pass_data(item_data[constants.Attributes.END.value]),
            betype=pass_data(item_data[constants.Attributes.BETYPE.value]),
            other_attribs=None)

    elif item_data[
        constants.Labels.TAG.value] == constants.ElementTags.FILE_CONTENT.value:
        content = None
        if item_data[
            constants.Labels.ELEMENT_TYPE.value] == constants.DataContentTypes.XML.value:
            content = mets.XMLData(
                item_data[constants.Labels.CONTENT.value])
        elif item_data[
            constants.Labels.ELEMENT_TYPE.value] == constants.DataContentTypes.BIN.value:
            content = mets.BinData(
                item_data[constants.Labels.CONTENT.value])

        element = mets.FileContent(content=content,
                                   element_id=pass_data(item_data[
                                                            constants.Attributes.ID.value]),
                                   use=pass_data(item_data[
                                                     constants.Attributes.USE.value]))

    elif item_data[
        constants.Labels.TAG.value] == constants.ElementTags.FILE_LOCATION.value:
        element = mets.FileLocation(
            loctype=pass_data(item_data[constants.Attributes.LOCTYPE.value]),
            xlink_href=pass_data(
                item_data[constants.Attributes.XLINK_HREF.value]),
            element_id=pass_data(item_data[constants.Attributes.ID.value]),
            use=pass_data(item_data[constants.Attributes.USE.value]),
            other_loctype=pass_data(
                item_data[constants.Attributes.OTHER_LOCTYPE.value]),
            xlink_role=pass_data(
                item_data[constants.Attributes.XLINK_ROLE.value]),
            xlink_arcrole=pass_data(
                item_data[constants.Attributes.XLINK_ARCROLE.value]),
            xlink_title=pass_data(
                item_data[constants.Attributes.XLINK_TITLE.value]),
            xlink_show=pass_data(
                item_data[constants.Attributes.XLINK_SHOW.value]),
            xlink_actuate=pass_data(
                item_data[constants.Attributes.XLINK_ACTUATE.value]))

    elif item_data[
        constants.Labels.TAG.value] == constants.ElementTags.STREAM.value:
        element = mets.Stream(
            element_id=pass_data(item_data[constants.Attributes.ID.value]),
            stream_type=pass_data(
                item_data[constants.Attributes.STREAM_TYPE.value]),
            owner_id=pass_data(item_data[constants.Attributes.OWNER_ID.value]),
            admid=pass_data(item_data[constants.Attributes.ADMID.value]),
            dmdid=pass_data(item_data[constants.Attributes.DMDID.value]),
            begin=pass_data(item_data[constants.Attributes.BEGIN.value]),
            end=pass_data(item_data[constants.Attributes.END.value]),
            betype=pass_data(item_data[constants.Attributes.BETYPE.value]))

    elif item_data[
        constants.Labels.TAG.value] == constants.ElementTags.TRANSFORM_FILE.value:
        element = mets.TransformFile(transform_type=pass_data(
            item_data[constants.Attributes.TRANSFORM_TYPE.value]),
            algorithm=pass_data(item_data[
                                    constants.Attributes.TRANSFORM_ALGORITHM.value]),
            order=int(pass_data(item_data[
                                    constants.Attributes.TRANSFORM_ORDER.value])),
            element_id=pass_data(item_data[
                                     constants.Attributes.ID.value]),
            key=pass_data(item_data[
                              constants.Attributes.TRANSFORM_KEY.value]),
            behavior=pass_data(item_data[
                                   constants.Attributes.TRANSFORM_BEHAVIOR.value]))

    return element


def transform_behaviour_element(item: QStandardItem) -> Union[
    mets.BehaviorSection,
    mets.Behavior,
    mets.ExecutableMechanism,
    mets.InterfaceDefinition]:
    element = None
    item_data = item.data(Qt.ItemDataRole.UserRole)

    if item_data[
        constants.Labels.TAG.value] == constants.ElementTags.BEHAVIOUR_SEC.value:
        content = []
        for i in range(item.rowCount()):
            content.append(transform_behaviour_element(item.child(i)))

        other_attribs = transform_other_attribs(
            item_data[constants.Labels.OTHER_ATTRIBS.value])

        element = mets.BehaviorSection(content=content,
                                       element_id=pass_data(item_data[
                                                                constants.Attributes.ID.value]),
                                       created=pass_data(item_data[
                                                             constants.Attributes.CREATED.value]),
                                       label=pass_data(item_data[
                                                           constants.Attributes.LABEL.value]),
                                       other_attribs=other_attribs)

    elif item_data[
        constants.Labels.TAG.value] == constants.ElementTags.BEHAVIOUR.value:
        content = []
        for i in range(item.rowCount()):
            content.append(transform_behaviour_element(item.child(i)))

        mechanism = None
        interface_def = None
        for child in content:
            if child.tag() == mets.ExecutableMechanism.tag():
                mechanism = child
            elif child.tag() == mets.InterfaceDefinition.tag():
                interface_def = child

        element = mets.Behavior(mechanism=mechanism,
                                element_id=pass_data(item_data[
                                                         constants.Attributes.ID.value]),
                                struct_id=pass_data(item_data[
                                                        constants.Attributes.STRUCTID.value]),
                                btype=pass_data(item_data[
                                                    constants.Attributes.BTYPE.value]),
                                created=pass_data(item_data[
                                                      constants.Attributes.CREATED.value]),
                                label=pass_data(item_data[
                                                    constants.Attributes.LABEL.value]),
                                group_id=pass_data(item_data[
                                                       constants.Attributes.GROUP_ID.value]),
                                admid=pass_data(item_data[
                                                    constants.Attributes.ADMID.value]),
                                interface_def=interface_def)

    elif item_data[
        constants.Labels.TAG.value] == constants.ElementTags.MECHANISM.value:
        element = mets.ExecutableMechanism(
            loctype=pass_data(item_data[constants.Attributes.LOCTYPE.value]),
            xlink_href=pass_data(
                item_data[constants.Attributes.XLINK_HREF.value]),
            element_id=pass_data(item_data[constants.Attributes.ID.value]),
            label=pass_data(item_data[constants.Attributes.LABEL.value]),
            other_loctype=pass_data(
                item_data[constants.Attributes.OTHER_LOCTYPE.value]),
            xlink_role=pass_data(
                item_data[constants.Attributes.XLINK_ROLE.value]),
            xlink_arcrole=pass_data(
                item_data[constants.Attributes.XLINK_ARCROLE.value]),
            xlink_title=pass_data(
                item_data[constants.Attributes.XLINK_TITLE.value]),
            xlink_show=pass_data(
                item_data[constants.Attributes.XLINK_SHOW.value]),
            xlink_actuate=pass_data(
                item_data[constants.Attributes.XLINK_ACTUATE.value]))

    elif item_data[
        constants.Labels.TAG.value] == constants.ElementTags.INTERFACE_DEFINITION.value:
        element = mets.InterfaceDefinition(
            loctype=pass_data(item_data[constants.Attributes.LOCTYPE.value]),
            xlink_href=pass_data(
                item_data[constants.Attributes.XLINK_HREF.value]),
            element_id=pass_data(item_data[constants.Attributes.ID.value]),
            label=pass_data(item_data[constants.Attributes.LABEL.value]),
            other_loctype=pass_data(
                item_data[constants.Attributes.OTHER_LOCTYPE.value]),
            xlink_role=pass_data(
                item_data[constants.Attributes.XLINK_ROLE.value]),
            xlink_arcrole=pass_data(
                item_data[constants.Attributes.XLINK_ARCROLE.value]),
            xlink_title=pass_data(
                item_data[constants.Attributes.XLINK_TITLE.value]),
            xlink_show=pass_data(
                item_data[constants.Attributes.XLINK_SHOW.value]),
            xlink_actuate=pass_data(
                item_data[constants.Attributes.XLINK_ACTUATE.value]))
    return element


# formatting function for other attributes
def transform_other_attribs(attrib_list: list[dict]) -> dict[str, str]:
    other_attribs = {}
    for attr in attrib_list:
        other_attribs[attr[constants.Attributes.NAME.value]] = attr[
            constants.Labels.VALUE.value]

    return other_attribs
