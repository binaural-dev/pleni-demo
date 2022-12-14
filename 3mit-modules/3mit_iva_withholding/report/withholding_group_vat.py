# coding: utf-8
###########################################################################

import time

#from odoo.report import report_sxw
#from odoo.tools.translate import _
from odoo import models, api, _
from odoo.exceptions import UserError, Warning, ValidationError

class IvaGroupReport(models.AbstractModel):
    _name = 'report.3mit_iva_withholding.template_wh_group_vat'
    _description = 'Report 3mit IVA withholding template withholding group vat'

    @api.model
    def _get_report_values(self, docids, data=None):
        if not docids:
            raise UserError("Se necesita seleccionar la data a Imprimir")
        data = {'form': self.env['wh.iva.group'].browse(docids)}
        res = dict()
        group_retention = data['form']
        lines = []
        total_general_doc = 0
        total_sum_base_general = 0
        total_sum_tax_general = 0
        total_sum_base_reducida = 0
        total_sum_tax_reducida = 0
        total_sum_base_additional = 0
        total_sum_tax_additional = 0
        base_exent_total = 0
        wh_tax_total_amount_general = 0
        document = None
        for wh_iva in group_retention.retentions:
            base_amount = []
            base_product = ''
            res_ali = []
            sum_base_general = 0
            sum_tax_general = 0
            sum_base_reducida = 0
            sum_tax_reducida = 0
            inv_nro_ctrl = ''
            inv_nro_fact = ''
            inv_refund = ''
            total_doc = 0
            inv_debit = ''
            sum_base_additional = 0
            sum_tax_additional = 0
            if wh_iva and len(wh_iva) ==1 :
                if wh_iva.state == 'done':
                    if (wh_iva.type == 'in_invoice' or wh_iva.type == 'in_refund' or wh_iva.type =='in_debit'):
                        if wh_iva.wh_lines:
                            base_product = 0
                            total_base_product = 0
                            total_base_exent = 0
                            total_amount_product = 0
                            base_exent = ' '

                        if wh_iva.wh_lines.type == 'in_invoice' or wh_iva.wh_lines.type == 'in_refund' or wh_iva.wh_lines.type == 'in_debit':


                            res_ali = []
                            total_alicuota = 0
                            base_product = 0
                            total_base_product = 0

                            total_amount_product = 0

                            base_general = 0
                            tax_general = 0
                            rate_general = ''
                            base_reducida = 0
                            tax_reducida = 0
                            rate_reducida = ''
                            base_additional = 0
                            tax_additional = 0
                            rate_additional = ' '
                            for line_tax in wh_iva.wh_lines.tax_line:


                                if not ((line_tax.alicuota == 16) and not (line_tax.alicuota == 8) and not (line_tax.alicuota == 31)) and line_tax.alicuota == 0:
                                    total_base_exent +=  line_tax.base
                                    base_exent = self.separador_cifra(total_base_exent)

                                if line_tax.alicuota == 16:
                                    base_general = line_tax.base
                                    tax_general = line_tax.amount
                                    rate_general = str(line_tax.alicuota)[0:2] + ' %'
                                    sum_base_general += line_tax.base
                                    sum_tax_general += line_tax.amount
                                if line_tax.alicuota == 8:
                                    base_reducida = line_tax.base
                                    tax_reducida = line_tax.amount_ret
                                    rate_reducida = str(line_tax.alicuota)[0:1] + ' %'
                                    sum_base_reducida += line_tax.base
                                    sum_tax_reducida += line_tax.amount
                                if line_tax.alicuota == 31:
                                    base_additional = line_tax.base
                                    tax_additional = line_tax.amount
                                    rate_additional = str(line_tax.alicuota)[0:2] + ' %'
                                    sum_base_additional += line_tax.base
                                    sum_tax_additional += line_tax.amount

                                total_base_product += line_tax.base
                                base_product = self.separador_cifra(total_base_product)
                                total_amount_product += line_tax.amount
                                amount_product = self.separador_cifra(total_amount_product)


                                # if line_tax.alicuota and not line_tax.alicuota == 0:
                                #   total_alicuota = line_tax.alicuota
                                #   alicuota = self.separador_cifra(total_alicuota)
                                if base_general > 0:
                                    base_general2 = self.separador_cifra(base_general)
                                else:
                                    base_general2 = ' '
                                if tax_general > 0:
                                    tax_general2 = self.separador_cifra(tax_general)
                                else:
                                    tax_general2 = ''

                                ######################3
                                if base_reducida > 0:
                                    base_reducida2 = self.separador_cifra(base_reducida)
                                else:
                                    base_reducida2 = ' '
                                if tax_reducida >0:
                                    tax_reducida2 = self.separador_cifra(tax_reducida)
                                else:
                                    tax_reducida2 = ' '

                                ###################3
                                if base_additional > 0:
                                    base_additional2 = self.separador_cifra(base_additional)
                                else:
                                    base_additional2 = ' '
                                if tax_additional > 0:
                                    tax_additional2 = self.separador_cifra(tax_additional)
                                else:
                                    tax_additional2 = ''

                                base_amount.append({'base_general':base_general2,
                                                    'tax_general' :tax_general2,
                                                    'rate_general': rate_general,
                                                    'base_reducida': base_reducida2,
                                                    'tax_reducida': tax_reducida2,
                                                    'rate_reducida': rate_reducida,
                                                    'base_additional': base_additional2,
                                                    'tax_additional': tax_additional2,
                                                    'rate_additional': rate_additional,
                                                    'base_exent': base_exent,
                                                    })




                        if wh_iva.wh_lines.invoice_id.move_type == 'in_refund':
                            inv_refund = wh_iva.wh_lines.invoice_id.supplier_invoice_number
                            inv_nro_fact = wh_iva.wh_lines.invoice_id.invoice_reverse_purchase_id.supplier_invoice_number
                            inv_nro_ctrl = wh_iva.wh_lines.invoice_id.nro_ctrl
                        elif wh_iva.wh_lines.type == 'in_debit':
                            factura_origin = self.env['account.move'].search([('id','=', wh_iva.wh_lines.invoice_id.debit_origin_id.id)])
                            inv_debit = wh_iva.wh_lines.invoice_id.supplier_invoice_number
                            inv_nro_fact = factura_origin.supplier_invoice_number
                            inv_nro_ctrl = wh_iva.wh_lines.invoice_id.nro_ctrl
                        elif  wh_iva.wh_lines.type == 'in_invoice':
                            inv_nro_ctrl = wh_iva.wh_lines.invoice_id.nro_ctrl

                    else:
                        raise UserError("El comprobante de Retencion de IVA se genera solo para los Proveedores")
                else:
                    raise UserError("La Retencion del IVA debe estar en estado Confirmado para poder generar su Comprobante")
            else:
                raise UserError("Solo puede seleccionar una Retencion de IVA a la vez, Por favor Seleccione una y proceda a Imprimir")
            partner_id = wh_iva.partner_id
            if partner_id.company_type == 'person':
                if partner_id.rif:
                    document = partner_id.rif
                else:
                    if partner_id.nationality == 'V' or partner_id.nationality == 'E':
                        document = str(partner_id.nationality) + str(partner_id.identification_id)
                    else:
                        document = str(partner_id.identification_id)
            else:
                if partner_id.rif:
                    document = partner_id.rif
                else:
                    document = 'N/A'
            if wh_iva.type == 'in_refund':
                total_sum_base_general = total_sum_base_general - float(sum_base_general)
                total_sum_tax_general = total_sum_tax_general - float(sum_tax_general)
                total_sum_base_reducida = total_sum_base_reducida - float(sum_base_reducida)
                total_sum_tax_reducida = total_sum_tax_reducida - float(sum_tax_reducida)
                total_sum_base_additional = total_sum_base_additional - float(sum_base_additional)
                total_sum_tax_additional = total_sum_tax_additional - float(sum_tax_additional)

            else:
                total_sum_base_general = total_sum_base_general + float(sum_base_general)
                total_sum_tax_general = total_sum_tax_general + float(sum_tax_general)
                total_sum_base_reducida = total_sum_base_reducida + float(sum_base_reducida)
                total_sum_tax_reducida = total_sum_tax_reducida + float(sum_tax_reducida)
                total_sum_base_additional = total_sum_base_additional + float(sum_base_additional)
                total_sum_tax_additional = total_sum_tax_additional + float(sum_tax_additional)
            fecha_op = wh_iva.wh_lines.invoice_id.invoice_date
            sum_base_general = self.separador_cifra(sum_base_general)
            sum_tax_general = self.separador_cifra(sum_tax_general)
            sum_base_reducida = self.separador_cifra(sum_base_reducida)
            sum_tax_reducida = self.separador_cifra(sum_tax_reducida)
            sum_base_additional = self.separador_cifra(sum_base_additional)
            sum_tax_additional = self.separador_cifra(sum_tax_additional)
            if wh_iva.state == 'done':
                if wh_iva.wh_lines.invoice_id.currency_id.id == wh_iva.company_id.currency_id.id :
                    total_doc = 0
                    for i in wh_iva.wh_lines.invoice_id.amount_by_group:
                        if i[0].find('IVA 16%') != -1 or i[0].find('IVA 8%') != -1 or i[0].find('IVA 15%') != -1:
                            total_doc = total_doc + (i[1])
                    total_doc = total_doc + (wh_iva.wh_lines.invoice_id.amount_untaxed)
                elif wh_iva.wh_lines.invoice_id.currency_id != wh_iva.company_id.currency_id.id:
                    tasa = wh_iva.wh_lines.invoice_id.currency_bs_rate
                    if tasa:
                        total_doc = 0
                        for i in wh_iva.wh_lines.invoice_id.amount_by_group:
                            if i[0].find('IVA 16%') != -1 or i[0].find('IVA 8%') != -1 or i[0].find('IVA 15%') != -1:
                                total_doc = total_doc + (i[1] * tasa)
                        total_doc = total_doc + (wh_iva.wh_lines.invoice_id.amount_untaxed * tasa )
                    else:
                        tasa = self.obtener_tasa(wh_iva.wh_lines.invoice_id)
                        total_doc = 0
                        for i in wh_iva.wh_lines.invoice_id.amount_by_group:
                            if i[0].find('IVA 16%') != -1 or i[0].find('IVA 8%') != -1 or i[0].find('IVA 15%') != -1:
                                total_doc = total_doc + (i[1] * tasa)
                        total_doc = total_doc + (wh_iva.wh_lines.invoice_id.amount_untaxed * tasa)

            base_exent_total = base_exent_total + total_base_exent
            if wh_iva.type == 'in_refund':
                wh_tax_total_amount_general = wh_tax_total_amount_general - float(wh_iva.total_tax_ret)
            else:
                wh_tax_total_amount_general = wh_tax_total_amount_general + float(wh_iva.total_tax_ret)
            if wh_iva.type == 'in_refund':
                total_general_doc = total_general_doc - total_doc
            else:
                total_general_doc = total_general_doc + total_doc
            line = {
                'fecha_op': fecha_op,
                'inv_nro_ctrl': inv_nro_ctrl,
                'inv_nro_fact': inv_nro_fact,
                'inv_refund': inv_refund,
                'inv_debit': inv_debit,
                'rate_general': rate_general,
                'rate_reducida': rate_reducida,
                'rate_additional': rate_additional,
                'base_amount': base_amount,
                'base_product': base_product,
                'base_exent': base_exent,
                'alicuota': res_ali,
                'total_doc': total_doc,
                'sum_base_general': sum_base_general,
                'sum_tax_general': sum_tax_general,
                'sum_base_reducida': sum_base_reducida,
                'sum_tax_reducida': sum_tax_reducida,
                'sum_base_additional': sum_base_additional,
                'sum_tax_additional': sum_tax_additional,
                'invoice': wh_iva.wh_lines.invoice_id,
                'total_tax_ret': wh_iva.total_tax_ret,
                'wh_iva_rate': wh_iva.wh_lines.wh_iva_rate,
            }
            lines.append(line)
        return {
            'data': data['form'],
            'model': self.env['report.3mit_iva_withholding.template_wh_group_vat'],
            'lines': lines, #self.get_lines(data.get('form')),
            #date.partner_id
            'document': document,
            'total_general_doc': total_general_doc,
            'total_sum_base_general': total_sum_base_general,
            'total_sum_tax_general': total_sum_tax_general,
            'total_sum_base_reducida': total_sum_base_reducida,
            'total_sum_tax_reducida': total_sum_tax_reducida,
            'total_sum_base_additional': total_sum_base_additional,
            'total_sum_tax_additional': total_sum_tax_additional,
            'base_exent_total': base_exent_total,
            'wh_tax_total_amount_general': wh_tax_total_amount_general,
        }

    def separador_cifra(self,valor):
        monto = '{0:,.2f}'.format(valor).replace('.', '-')
        monto = monto.replace(',', '.')
        monto = monto.replace('-', ',')
        return  monto

    def get_period(self, date):
        if not date:
            raise Warning (_("You need date."))
        split_date = (str(date).split('-'))
        return str(split_date[1]) + '/' + str(split_date[0])

    def get_date(self, date):
        if not date:
            raise Warning(_("You need date."))
        split_date = (str(date).split('-'))
        return str(split_date[2]) + '/' + (split_date[1]) + '/' + str(split_date[0])

    def get_direction(self, partner):
        direction = ''
        direction = ((partner.street and partner.street + ', ') or '') +\
                    ((partner.street2 and partner.street2 + ', ') or '') +\
                    ((partner.city and partner.city + ', ') or '') +\
                    ((partner.state_id.name and partner.state_id.name + ',')or '')+ \
                    ((partner.country_id.name and partner.country_id.name + '') or '')
        #if direction == '':
        #    raise ValidationError ("Debe ingresar los datos de direccion en el proveedor")
            #direction = 'Sin direccion'
        return direction

    def get_tipo_doc(self, tipo=None):
        if not tipo:
            return []
        types = {'out_invoice': '1', 'in_invoice': '1', 'out_refund': '2',
                 'in_refund': '2'}
        return types[tipo]

    def get_t_type(self, doc_type=None, name=None):
        tt = ''
        if doc_type:
            if doc_type == "in_debit" or doc_type == "out_debit":
                tt = '02-COMP'
            elif name and name.find('PAPELANULADO') >= 0:
                tt = '03-ANU'
            if doc_type == "out_refund" or doc_type == "in_refund":
                tt = '03'
            elif doc_type == "in_invoice" or doc_type == "out_invoice":
                tt = '01-REG'
        return tt



